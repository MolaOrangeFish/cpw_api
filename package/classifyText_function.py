import numpy as np
from package.sql_connector import * 
from package.nlp_function import *
from app import *
import joblib
#from bag_of_word import *

# LOAD SEGMENTATION MODEL
# 0:Negative 1:Positive 2:Question
segment_type = "model/segment_classify/check_segment_type.sav"
segment_vectorizer = "model/segment_classify/segment_vectorizer_word.sav"
segment_model = joblib.load(open(segment_type, "rb"))
vectorizer_segment = joblib.load(open(segment_vectorizer, "rb"))

# LOAD QUESTION MODEL
# 0:ค่าเทอม 1:Other
question_type = "model/question_classify/check_question_type.sav"
question_vectorizer = "model/question_classify/question_vectorizer_word.sav"
question_model = joblib.load(open(question_type, "rb"))
vectorizer_question = joblib.load(open(question_vectorizer, "rb"))

def split_text(message):
    print("#######Get in spilt_text######")
    split_text = split_word(message)
    print(f"text:{split_text}")    
    return split_text

def split_text_ai(message):    
    print("#######Get in spilt_text_ai######")
    split_text_ai = str(split_word(message))
    split_text_ai = text_process_save_comma(split_text_ai)
    print(f"ai:{split_text_ai}")
    return split_text_ai

# FUNCTION SEGMENTATION MODEL
def classifySegment(text):

    #if "สวัสดี" in text:
    #    feedback = "โรงเรียนชลประทานสวัสดีค่ะ ต้องการติดต่อด้านไหนคะ"
    #    return (feedback,"Greeting",True)
    
    text_list = vectorizer_segment.transform([text]).reshape(1,-1).todense()  # นำข้อความที่ถูกแบ่งคำแล้ว (text) มาใช้ vectorizer (vectorizer_question) ในการแปลงเป็น vector โดยใช้ transform และ reshape เพื่อเตรียมข้อมูลและแปลงเป็น dense matrix ด้วย todense().
    predictions = segment_model.predict(np.asarray(text_list))                 # ทำนายประเภทของคำถาม (question type) โดยใช้โมเดลที่โหลดมา (question_model) และข้อมูลที่เตรียมไว้ (text_list) โดยใช้ predict 

    # 0:Negative 1:Positive 2:Question
    if(predictions[0]==0): 
        print('Negative Group')
        feedback = get_answer("negative")
        return (feedback,"negative",True)
    elif (predictions[0]==1):
        print('Positive Group')
        feedback = get_answer("positive")
        return (feedback,"positive",True)
    else:
        print('Question Group')
        return classifyQuestion(text)
        

# FUNCTION QUESTION MODEL
def classifyQuestion(text):

    text_list = vectorizer_question.transform([text]).reshape(1, -1).todense()
    question_predictions = question_model.predict(np.asarray(text_list))
    question_type = str(question_predictions[0])
    print(f"Prediction: {question_type}")

    menu = " "
    
    if question_type == "1":      ### type 1 == ฝ่ายวิชาการ / โครงการพิเศษ / EP ###
        menu = get_answer("question",question_type)
    elif question_type == "2":    ### type 2 == ฝ่ายโภชนาการ / พัสดุ / สหกรณ์ ### 
        menu = get_answer("question",question_type)
    elif question_type == "3":    ### type 3 == ฝ่ายปกครอง / กิจการนักเรียน /  กิจกรรมต่างๆ โครงการภายใน-นอก ##
        menu = get_answer("question",question_type)
    elif question_type == "4":    ### type 4 == ฝ่ายธุรการ / ฝ่ายบัญชี / บริหาร ###
        menu = get_answer("question",question_type)
    elif question_type == "5":    ### type 5 == ศูนย์พัฒนาโรงเรียนดิจิทัล ###
        menu = get_answer("question",question_type)
    else:                       ### type 0 == ไม่เกี่ยวข้อง ###
        menu = get_answer("question",question_type)

    return (menu,"question"+question_type,True)





    
