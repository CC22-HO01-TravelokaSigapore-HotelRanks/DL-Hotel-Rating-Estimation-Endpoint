# [For You Page] Deep Learning Rating Estimation Endpoint

This is only an endpoint for one of the pipeline to optimize Hotel Ranking.

## Location Recognition Endpoint

This is only an endpoint for one of the pipeline to optimize Hotel Ranking.  

| Information  | Value                                  |
|--------------|----------------------------------------|
| Docker Image | [kaenova/traveloka-dl-rating-estimation](https://hub.docker.com/r/kaenova/traveloka-dl-rating-estimation) |
|   Port Open  |                  8001                  |

## Environment Variables
| Variables   | Description                      |
|-------------|----------------------------------|
| DB_USER     | Database Username                |
| DB_PASSWORD | Database Password                |
| DB_HOST     | Database IP Address or Host name |
| DB_PORT     | Database Port                    |
| DB_NAME     | Database Name                    |
| DB_CON_STRING     | Database Connection String (if used, will ignore all DB ENV above)                   |
| REDIS_HOST     | Redis Host (Leave it empty if you want to use internal redis)                    |
| REDIS_PORT     | Redis Port (Leave it empty if you want to use internal redis)                    |

## APIs
| Endpoint | Method |           Body Sent (JSON)          |                 Description                |
|:--------:|:------:|:-----------------------------------:|:------------------------------------------:|
|     /    |   GET  |                 None                |            Hello World Endpoint            |
|     /    |  POST  | {"user_id" : 10, "longitude": -100.0, "latitude": 90.5} | Will Return a List of hotel ids recommended |

Checkout all our pre-trained model through this [link](https://drive.google.com/drive/folders/1-2S6UhR6bZY90j89c8cpScCcpCJJBEal?usp=sharing).  

CC22-HO01 ML Teams.