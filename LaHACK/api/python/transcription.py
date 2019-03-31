from google.cloud import videointelligence_v1p1beta1 as videointelligence
import pickle
import sys
import os

credential_path = "/Users/joann/Desktop/LAHacks/LA-Hacks-ba0160311e2d.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def Request(input_uri):
    print(input_uri)
    video_client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code='en-US',
        enable_automatic_punctuation=True)

    video_context = videointelligence.types.VideoContext(
        speech_transcription_config=config)

    operation = video_client.annotate_video(
        input_uri, features=features,
        video_context=video_context)

    #print('\nProcessing video for speech transcription.')

    result = operation.result(timeout=180)
    return result


def generate_sentence(result):
    annotation_results = result.annotation_results[0]

    sentence = []
    time_code = []
    start_time = 0
    end_time = 0

    for speech_transcription in annotation_results.speech_transcriptions:
        alternative = speech_transcription.alternatives[0]

        wrd = []
        for word_info in alternative.words:
            start = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
            end = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9

            if(len(wrd) == 0):
                start_time = start

            word = word_info.word
            wrd.append(word)
        
            if(word[-1] == '.'):
                sentence.append(wrd)
                wrd = []
                end_time = end
                time_code.append((start_time, end_time))

    return (sentence, time_code)


def dump_file(sentence, time_code, video):
    file = open(video + '.pkl', 'wb')
    pickle.dump((sentence, time_code), file,)

from moviepy.editor import *

video = sys.argv[1]
video_file = "api/python/" + video + '.mp4'
my_clip = VideoFileClip(video_file)
input_uri = 'gs://la-hacks-236102-lcm/' + video + '.mp4'
keyword = sys.argv[2]

try:
    file = open(video + '.pkl', 'rb')
    (sentence, time_code) = pickle.load(file)
except:
    result = Request(input_uri)
    (sentence, time_code) = generate_sentence(result)
    dump_file(sentence, time_code, video)
    pass

_ret = []

n = 0

for i in range(len(sentence)):
    for word in sentence[i]:
        word = word.split('.')[0]
        w1 = word.lower()
        w2 = keyword.lower()
        if(len(w1) <= len(w2)+1 and w2 in w1):
            _ret.append((sentence[i], time_code[i]))
            time = (time_code[i][0] + time_code[i][1])/2
            frame_file = 'static/img/' + video + '_' + str(n) + '_transcription.png'
            my_clip.save_frame(frame_file, t = time)
            n += 1
            break

#print('Tested video:', video, ', keyword:', keyword)

for i in range(len(_ret)):
    #print('return #{}:'.format(i+1))
    sentence = _ret[i][0]
    time_code = _ret[i][1]

    _str = ''
    for word in sentence:
        _str = _str + ' ' + word

    #print('Sentence:', _str)
    start_time = time_code[0]
    end_time = time_code[1]
    #print('Start:', start_time, 'End:', end_time)

print_str = '{' + '\"{}\":['.format(keyword)

for i in range(len(_ret)):
    sentence = _ret[i][0]
    time_code = _ret[i][1]
    print_str += '{'
    _str = ''
    for word in sentence:
        _str = _str + ' ' + word

    print_str += '\"sentence\": \"{}\",\"time\": {},\"img\": \"img/{}_{}_transcription.png\"'.format(_str, time_code[0], video, str(i))
    print_str += '}'
    if(not i == len(_ret)-1):
        print_str += ','

print_str += ']' + '}'
print(print_str)
