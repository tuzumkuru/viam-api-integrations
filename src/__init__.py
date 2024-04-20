"""
This file registers the model with the Python SDK.
"""

from viam.services.vision import Vision
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .plantnet.plantnet_api import plantnetApi

Registry.register_resource_creator(Vision.SUBTYPE, plantnetApi.MODEL, ResourceCreatorRegistration(plantnetApi.new, plantnetApi.validate))
