from flask import Flask,request
import joblib
import numpy as np
# from package.sql_connector import *
from package.nlp_function import *
# 0:Negative 1:Positive 2:Question
segment_type = "segment_classify/check_segment_type.sav"
segment_vectorizer = "segment_classify/segment_vectorizer_word.sav"
segment_model = joblib.load(open(segment_type,"rb"))
vectorizer_segment = joblib.load(open(segment_vectorizer,"rb"))

# LOAD QEUSTION MODEL
# 0: 1: 2: 3: 4: 5:
question_type = "question_classify/check_question_type.sav"
question_vectorizer = "question_classify/question_vectorizer_word.sav"
question_model = joblib.load(open(question_type,"rb"))
vectorizer_question = joblib.load(open(question_vectorizer,"rb"))

app = Flask(__name__)

@app.route("/getSegment", methods=['POST'])
def Segment():
    request_data = request.get_json()

    replyFromUser = request_data["reply"]
    split_text_ai=text_process_save_comma(str(split_word(replyFromUser))) 

    text_list = vectorizer_segment.transform([split_text_ai]).reshape(1,-1).todense()  # นำข้อความที่ถูกแบ่งคำแล้ว (split_text_ai) มาใช้ vectorizer (vectorizer_question) ในการแปลงเป็น vector โดยใช้ transform และ reshape เพื่อเตรียมข้อมูลและแปลงเป็น dense matrix ด้วย todense().
    predictions = segment_model.predict(np.asarray(text_list)) 
    if(predictions[0]==0): 
        description = "negative"
    elif (predictions[0]==1):
        description = "positive"
    else:
        description = "question"
    data={ 
            "cutword": split_text_ai,
            "segmentType": str(predictions[0]),
            "description": description
        } 
    return data 

@app.route("/getMainQuestionType", methods=['POST'])
def mainQuesType():
    request_data = request.get_json()

    replyFromUser = request_data["reply"]
    split_text_ai=text_process_save_comma(str(split_word(replyFromUser))) 
    text_list = vectorizer_question.transform([split_text_ai]).reshape(1,-1).todense() 
    predictions = question_model.predict(np.asarray(text_list))   
    if(predictions[0]==1): 
        description = "วิชาการ"
        feedback = "คุณต้องการติดต่อบริการด้านอะไร 1.ตารางเรียน 2.ตารางสอบ 3.หลักสูตร 4.ฟอร์มแบบคำร้องขอหลักฐานการศึกษา 5.อื่นๆ ติดต่อสอบถามเพิ่มเติม"
    elif (predictions[0]==2):
        description = "โภชนาการ"
        feedback = "คุณต้องการติดต่อบริการด้านอะไร 1.เมนูอาหารกลางวันประจำสัปดาห์ 2.สหกรณ์โรงเรียนชลประทานวิทยา 3.ลานจอดรถใหม่สนามกอล์ฟชลประทาน 4.อื่นๆ ติดต่อสอบถามเพิ่มเติม"
    elif (predictions[0]==3):
        description = "ปกครอง"
        feedback = "คุณต้องการติดต่อบริการด้านอะไร 1.ระเบียบการแต่งกายของนักเรียน 2.กิจกรรมนักเรียน 3.นักศึกษาวิชาทหาร 4.อื่นๆ ติดต่อสอบถามเพิ่มเติม"
    elif (predictions[0]==4):
        description = "ธุรการ"
        feedback = "คุณต้องการติดต่อบริการด้านอะไร 1.สมัครเรียน 2.สมัครบุคลากร 3.ค่าธรรมเนียมการศึกษา 4.อื่นๆ ติดต่อสอบถามเพิ่มเติม"
    elif (predictions[0]==5):
        description = "สารสนเทศ" 
        feedback = "คุณต้องการติดต่อบริการด้านอะไร 1.ศูนย์ฝึกว่ายน้ำ 2.ระบบชำระเงิน 3.ประกาศผลการเรียน 4.ระบบรถรับ-ส่ง 5.ระบบโรงอาหารอื่นๆ 6.CPW School Application 7.ติดต่อสอบถามเพิ่มเติม"      
    else:
        description = "รอสักครู่ ฉันจะรีบติดต่อกลับไปให้เร็วที่สุดนะคะ / I’ll get back to you as soon as possible"          

    data={ 
            "cutword": split_text_ai,
            "mainQuesType": str(predictions[0]),
            "feedback":feedback,
            "description": description
        } 
    return data 

# @app.route("/getSubQuestionType", methods=['POST'])
# def subQuesType():

if __name__ =="__main__":
    app.run(debug=True)