from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from PIL import Image

from viam.media.video import RawImage
from viam.proto.common import PointCloudObject
from viam.proto.service.vision import Classification, Detection
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype


from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.camera import Camera

from viam.services.vision import Vision
from viam.logging import getLogger

import time
import asyncio
import requests
import io

LOGGER = getLogger(__name__)

class plantnetApi(Vision, Reconfigurable):
    
    """
    Vision represents a Vision service.
    """    

    MODEL: ClassVar[Model] = Model(ModelFamily("tuzumkuru", "viam-api-integrations"), "plantnet-api")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    # some_pin: int
    api_key: str
    project: str

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        LOGGER.debug("running plantnetApi.new()")
        new_class = cls(config.name)
        new_class.reconfigure(config, dependencies)
        return new_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        LOGGER.debug("running plantnetApi.validate()")

        if not str(config.attributes.fields["api_key"].string_value):
            raise Exception("An api_key must be defined")
        
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        LOGGER.debug("running plantnetApi.reconfigure()")

        self.api_key = str(config.attributes.fields["api_key"].string_value)

        if not str(config.attributes.fields["project"].string_value):
             self.project = "all"
        else:
             self.project = str(config.attributes.fields["project"].string_value)

        return  

    # Implement the methods the Viam RDK defines for the Vision API (rdk:service:vision)
    async def get_detections_from_camera(
        self,
        camera_name: str,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        LOGGER.debug("running plantnetApi.get_detections_from_camera()")
        
        camera_resource = Camera.get_resource_name(camera_name)

        if (camera_resource not in self.DEPS):
            raise Exception("Camera resource not found")
        
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]

        cam = cast(Camera, actual_cam)

        cam_image = await cam.get_image()

        return await self.get_detections(image=cam_image)
    
    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        LOGGER.debug("running plantnetApi.get_detections()")

        detectionList = []

        # Get a classification and use it to create a detection with a box of the whole image size
        classifications = await self.get_classifications(image,count = 1)

        for classification in classifications:
            detectionList.append(Detection(x_min=0, x_max=image.width, y_min=0, y_max=image.height, class_name=classification.class_name, confidence=classification.confidence))

        return detectionList

    
    async def get_classifications_from_camera(
        self,
        camera_name: str,
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        LOGGER.info("running plantnetApi.get_classifications_from_camera()")

        camera_resource = Camera.get_resource_name(camera_name)

        if (camera_resource not in self.DEPS):
            raise Exception("Camera resource not found")
        
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]

        cam = cast(Camera, actual_cam)

        cam_image = await cam.get_image()

        return await self.get_classifications(image=cam_image)

    
    async def get_classifications(
        self,
        image: Union[Image.Image, RawImage],
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        LOGGER.debug("running plantnetApi.get_classifications()")

        return await self.identify_plants(image, count=count)

    
    async def get_object_point_clouds(
        self,
        camera_name: str,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[PointCloudObject]:
        LOGGER.debug("running plantnetApi.get_object_point_clouds()")
        raise NotImplementedError("Method is not available for this module")


    async def identify_plants(self, image: Union[Image.Image, RawImage], count: int = 1) -> List[Classification]:
        # Send image to PlantNet API
        api_endpoint = f"https://my-api.plantnet.org/v2/identify/{self.project}?api-key={self.api_key}"

        # Convert image to JPEG format
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='JPEG')
        image_bytes = img_byte_array.getvalue()

        files = {'images': image_bytes}
        response = requests.post(api_endpoint, files=files)

        if response.status_code == 200:
            # Parse API response
            json_result = response.json()
            plant_identifications = []
            for result in json_result['results'][:count]:
                classification = Classification(
                    class_name=result['species']['scientificName'],
                    confidence=result['score']
                )
                plant_identifications.append(classification)
            return plant_identifications
        else:
            # Handle API error
            LOGGER.error(f"Error occurred while identifying plants: {response.text}")
            return []
