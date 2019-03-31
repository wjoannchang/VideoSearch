# VideoSearch

## Inspiration
Sometimes we don't want to watch the entire video but just interested in some highlighted segments. We hope somebody can label timeline for us. Therefore, it will be convenient if we can segment the videos automatically. 

## What it does
It provides the service of searching content in a video. It extracts both video and voice information into high level features. Then, users can search with keyword based on the context of the video. It will return suitable timestamps for the user to explore the video in a more convenience way.

## How I built it
We analyze the input videos with google cloud vision API. The API will give us the transcriptions and the labels of entities in the videos. We utilize the transcriptions and object labels to match the keywords users want to search in the videos. Once the search is done, the time codes are sent to our server. Based on the time codes, we are able to extract the video segments from the YouTube.

## Challenges I ran into
* Analyze videos requires time if we don't create a cache to save the previous results
* Dependencies between developers
* Lack of UI/UX design experience

## Accomplishments that I'm proud of
* Accurate and real-time searching results
* Both visual and semantic features can be retrieved
* A clean and user-friendly interface

## What I learned
* Usage of google cloud vision API
* Deploy python scripts on node.js
* Build RESTful API on node.js backend
* Set up a VM on google cloud platform
* How to be a good front-end engineer in three days :)

## What's next for SearchIn Video
* We hope to extend more features that users can search for. For instance, if we can find when a certain person appears in the video will be cool!
* Implement our system entirely on the cloud.
