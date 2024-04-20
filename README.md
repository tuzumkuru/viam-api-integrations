# plantnet-api modular service

This module implements the [rdk vision API](https://github.com/rdk/vision-api) in a tuzumkuru:viam-api-integrations:plantnet-api model.
Using this model as a vision service, you can make API calls to [Pl@ntNet API](https://plantnet.org) to classify plant images.

## Requirements

Pl@ntNet Account 

``` bash
```

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:vision:tuzumkuru:viam-api-integrations:plantnet-api` model from the [`tuzumkuru:viam-api-integrations:plantnet-api` module](https://app.viam.com/module/rdk/tuzumkuru:viam-api-integrations:plantnet-api).

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
| `project` | string | Optional |  TODO |

### Example Configuration

```json
{
  TODO: INSERT SAMPLE CONFIGURATION(S)
}
```

### Next Steps

_Add any additional information you want readers to know and direct them towards what to do next with this module._
_For example:_ 

- To test your...
- To write code against your...

## Troubleshooting

_Add troubleshooting notes here._
