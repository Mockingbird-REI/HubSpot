A Quick summary on how to use while we develop documentation.

# An Introduction
The Client Class is your Friend.  Start here for pretty much everything

``` Python
from typing import List

from HubSpot.CRM import Client, DEAL, HubSpotObject, NOTE

client = client(APP_TOKEN)
```

Once your client is set up, you can start interacting with HubSpot by listing objects or pipelines...

``` Python
deals: List = list(client.get_objects(DEAL)
pipelines: List = list(client.list_pipelines(DEAL))
```

...creating objects...
``` Python
# Creating a new deal ("New Deal") in the pipeline "My Pipeline"
my_pipeline = [pipeline for pipeline in pipelines if pipeline.label == "My Pipeline"][0]

new_deal_properties = {
    "dealname": "New Deal",
    "dealstage": pipeline.stages[0],
    "dealpipeline": pipeline.label,
}
new_deal: HubSpotObject = client.new_object(DEAL, new_deal_properties)
```

...or even interacting with objects directly!
``` Python
# Creating a Note to add to the newly created deal.

# Where creation of an object requires a timestamp (hs_timestamp), the current 
# time is used if a timestamp isnt specified.
new_note_properties = {
    "hs_note_body": "I Love Notes!"
}
new_note = client.new_object(NOTE, new_note_properties)

new_deal.associate(new_note)
```

Developed on Python 3.8
