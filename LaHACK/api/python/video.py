from google.cloud import videointelligence
import os
import sys
import pickle
from moviepy.editor import *

credential_path = "/Users/joann/Desktop/LAHacks/LA-Hacks-ba0160311e2d.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def Request(path):

    """ Detects labels given a GCS path. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]

    mode = videointelligence.enums.LabelDetectionMode.SHOT_AND_FRAME_MODE
    config = videointelligence.types.LabelDetectionConfig(
        label_detection_mode=mode)
    context = videointelligence.types.VideoContext(
        label_detection_config=config)

    operation = video_client.annotate_video(
        path, features=features, video_context=context)
    # print('\nProcessing video for label annotations:')

    result = operation.result(timeout=270)
    # print('\nFinished processing.')

    return result

def generate_output(result):
    output = {}
    # Process frame level label annotations
    frame_labels = result.annotation_results[0].frame_label_annotations
    for i, frame_label in enumerate(frame_labels):
        frame = frame_label.frames[0]
        time_offset = (frame.time_offset.seconds +
                    frame.time_offset.nanos / 1e9)
        if frame_label.entity.description in output:
            output[frame_label.entity.description].append(time_offset)
        else:
            output[frame_label.entity.description] = [time_offset]

    target = sys.argv[2]
    if target in output:
        result = output[target]
    else:
        result = []

    # msg = "{\""+target+"\":"+str(result)+"}"
    
    return result

def dump_file(metadata, video):
    with open(str(video)+".pkl", 'wb') as file:
        pickle.dump(metadata, file,)

v = sys.argv[1].split("/")[-1].split(".")[0]
video = v+"_video"


try:
    file = open(str(video)+".pkl", 'rb')
    metadata = pickle.load(file)
    file.close()
except:
    metadata = Request(sys.argv[1])
    dump_file(metadata, video)
    pass

result_time = generate_output(metadata)
msg = "{\""+sys.argv[2]+"\":["

video_file = 'api/python/' + v + '.mp4'
my_clip = VideoFileClip(video_file)

for i, time in enumerate(result_time):
    frame_file = "static/img/" + video + '_' + str(i)+'_video.png'
    my_clip.save_frame(frame_file, t = time+3)
    msg += "{\"time\":"+str(time)+","+"\"img\":\""+ "img/" + video + '_' + str(i)+'_video.png' +"\"}"
msg += "]}"
print(msg)
sys.stdout.flush()