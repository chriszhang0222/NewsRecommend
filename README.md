# NewsRecommend System

- Implemented a web crawler and a data pipeline which monitors, scrapes and dedupes latest news into MongoDB from difference news sources(MongoDB, Redis, RabbitMQ);
- Built a single-page web application for users to browse, search news, and give user recommendation (React, Node.js, SOA, JWT);
- Built the backend RPC service with python SimpleJSONRPCServer, including user service, recommend service, news service, machine learning service
- Implemented a click event log processor which collects users’ click logs, then updates a news preference model for
each user. Do the recommendation to different user based on their user preference model (NLP);
- Utilized Redis and tensorflow TF-IDF to achieve the news deduplication
- Designed and built an Convolution Nerual Network based offline training pipeline for news topic modeling (Tensorflow, CNN, NLP);
- Deployed an online classifying service for news topic modeling using the trained model.

### Skills:
- JavaScript, Python, React, Node.js, Express, Redis, MongoDB, RabbitMQ, RPC, Tensorflow, NLP, Docker
