# plantnet-api modular service

This module implements the [rdk vision API](https://github.com/rdk/vision-api) in a tuzumkuru:viam-api-integrations:plantnet-api model.
Using this model as a vision service, you can make API calls to [Pl@ntNet API](https://plantnet.org) to classify plant images.

## Requirements

Pl@ntNet Account 

``` bash
```

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `vision / api-integrations:plantnet-api` model from the [`tuzumkuru:api-integrations` module](https://app.viam.com/module/tuzumkuru/api-integrations).

## Configure your vision

> [!NOTE]  
> Before configuring your vision, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `vision` type, then select the `tuzumkuru:viam-api-integrations:plantnet-api` model. 
Enter a name for your vision and click **Create**.

On the new component panel, copy and paste the following attribute template into your vision’s **Attributes** box:

```json
{
  "api_key": "<<your-api-key-here>>",
  "project": "all" 
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:vision:tuzumkuru:viam-api-integrations:plantnet-api` visions:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `api_key` | string | **Required** |  API key from [Pl@ntNet profile settings page](https://my.plantnet.org/account/settings). |
| `project` | string | Optional |  A project type for the API call. The default value is `all`. Details below |

The API uses projects for different data sets, i.e. floras. Choosing a specific flora would make the classification more accurate. The following table describes some of the available projects/floras:

| ID          | Title                                     | Description                                                                       |
|-------------|-------------------------------------------|-----------------------------------------------------------------------------------|
| all         | All projects                              | Includes all of the below projects                                                 |
| the-plant-list | World flora                           | Species of the World flora                                                        |
| weeds       | Weeds                                     | Weeds in agricultural fields of Europe                                            |
| invasion    | Invasive plants                           | Invasive species potentially threatening livelihoods and the environment worldwide |
| prosea      | Useful plants of Asia                    | Plant Resources of South East Asia                                                |
| useful      | Useful plants                             | Cultivated and ornamental plants                                                  |
| prota       | Useful plants of Tropical Africa          | Plant Resources of Tropical Africa                                                |
| weurope     | Western Europe                            | Plants of Western Europe                                                          |
| martiniuqe  | Martinique                                | Plants of Martinique Island                                                       |
| lapaz       | Tropical Andes                            | Plants of the La Paz Valley, Bolivia                                               |
| namerica    | USA                                       | Plants of the United States                                                        |

You can find more with an API call, details are [here](https://my-api.plantnet.org/#/my-api/getV2Projects)

### Example Configuration

```json
{
  "api_key": "<<your-api-key-here>>",
  "project": "all" 
}
```

### Next Steps

- Add more configuration parameters to be used with the API

## Troubleshooting

- No known errors till now. Please report any issues you find. 
