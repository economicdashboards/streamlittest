import datetime
import sys
import time
import streamlit as st
import logging
from time import sleep

def todigits(s, n):
  s = s.strip()
  s = '0000000000'+s
  s = s[len(s)-n:len(s)].strip()
  return s

def datestring():
  ct = datetime.datetime.now()
  dt = todigits(str(ct.year),4) + '-' + todigits(str(ct.month),2)+ '-' + todigits(str(ct.day),2)+ '-' + todigits(str(ct.hour),2)+ '-' + todigits(str(ct.minute),2)+ '-' + todigits(str(ct.second),2)
  return dt

def runsqlstatement(ssql):
  r = ''
  try:
    connection = mysql.connector.connect(host='sql5.freemysqlhosting.net',
                                         database='sql5521302',
                                         user='sql5521302',
                                         password='TvCHYlcKBJ'
                                  )
    if connection.is_connected():
        #print("MySQL connection is opened")
        cursor = connection.cursor()
        cursor.execute(ssql)
        connection.commit()
        r = 'Executed : ' + ssql
        #print(r)
  except Error as e:
        r = "Error while executing : L"+ ssql + " ---- "
        print("Error while executing : L"+ ssql + " ---- ", e)
  finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
  return r

def addquestion(question, engines, keywords):
  ds = datestring()
  questionid = ''
  question = question.strip().lower()
  engines = engines.strip().lower()
  keywords = keywords.strip().lower()
  if (len(question)  >0) & (len(engines)  >0):
        for engine in engines.split(";"):
          engine = engine.strip()
          if len(engine) > 0:
            questionid = question + ' @ ' + ds
            ssql = "INSERT INTO questions (questionuniqueid, question, askdate, rengine, keywords, answered, markforarchiving) VALUES ('" + questionid.replace("'","''")
            ssql = ssql + "','" + question.replace("'","''") + "','" + ds + "','" + engine.replace("'","''") + "','" + keywords.replace("'","''") + "',0,0)"
            #print(ssql)
            x = runsqlstatement(ssql)
  return questionid

createanswerstablesql  = 'CREATE TABLE IF NOT EXISTS answers (questionuniqueid varchar(255),  question varchar(255), askdate varchar(255), engine varchar(255), keywords varchar(255), answerno int, answertitle varchar(255), anwershort varchar(255), answerlong varchar(255), answerdate varchar(255), markforarchiving int);'
createquestionstablesql = 'CREATE TABLE IF NOT EXISTS questions (questionuniqueid varchar(255),  question varchar(255), askdate varchar(255), rengine varchar(255), keywords varchar(255), answered int, markforarchiving int);'


def getfirstUnansweredQuestion(engine):
  rv = []
  engine = engine.lower().strip()
  if len(engine) > 0:
      ssql = "SELECT questionuniqueid, question FROM questions WHERE answered=0 AND rengine='"+engine.replace("'","''")+"' ORDER BY askdate"
      try:
        connection = mysql.connector.connect(host='sql5.freemysqlhosting.net',
                                            database='sql5521302',
                                            user='sql5521302',
                                            password='TvCHYlcKBJ'
                                      )
        if connection.is_connected():
            #print("MySQL connection is opened")
            cursor = connection.cursor()#
            cursor.execute(ssql)
            records = cursor.fetchall()
            #print(records)
            if len(records) > 0:
              rv = (records[0])
            r = 'Executed : ' + ssql
            print(r)
      except Error as e:
            r = "Error while executing : L"+ ssql + " ---- "
            print("Error while executing : L"+ ssql + " ---- ", e)
      finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                #print("MySQL connection is closed")
      return rv

def addanswer(questionid, answertitle, answershort, answerlong, answerno, engine):
  #questionid = 'what is a question? @ 2022-09-21-17-46-36'
  #answertitle= 'i'
  #answershort = 'a form of interrogation'
  #answerlong = 'a question is a form of interrogation'
  #answerno = 8
  ds = datestring()
  questionid = questionid.strip().lower()
  answershort = answershort.strip().lower()
  answerlong = answerlong.strip().lower()
  engine = engine.strip().lower()
  if (len(questionid) > 0) & (len(answershort+answertitle+answerlong) > 0):
      ssql ="INSERT INTO answers(questionuniqueid, question, askdate, engine, keywords, answerno, answertitle, anwershort, answerlong, answerdate, markforarchiving)"
      ssql = ssql + " SELECT questionuniqueid, question, askdate, rengine AS engine, keywords, "+str(answerno)+" AS anwerno, '"+answertitle.replace("'","''")+"' AS answertitle,'"+answershort.replace("'","''")+"' AS anwershort,'"+answerlong.replace("'","''")+"' AS answerlong,'"+ds.replace("'","''")+"' AS answerdate,0 AS markforarchiving FROM questions WHERE questionuniqueid='"+questionid.replace("'","''")+"' AND rengine='"+engine.replace("'","''")+"'"
      #print(ssql)
      x = runsqlstatement(ssql)
  return 0

def markquestionasanswered(questionid, engine):
    questionid = questionid.lower().strip()
    engine = engine.lower().strip()
    if (len(questionid) > 0) & (len(engine) > 0):
        ssql = "UPDATE questions SET answered=1 WHERE questionuniqueid='"+questionid.replace("'","''")+"' AND rengine='"+engine.replace("'","''")+"'"
        x = runsqlstatement(ssql)
    return 0

def isquestionanswered(questionid, engine):
    rv = False
    questionid = questionid.strip().lower()
    engine = engine.strip().lower()
    if (len(questionid) > 0) & (len(engine) > 0):
          ssql = "SELECT * FROM questions WHERE questionuniqueid='"+questionid.replace("'","''")+"' and rengine='"+engine.replace("'","''")+"' AND answered=1"#
          try:
            connection = mysql.connector.connect(host='sql5.freemysqlhosting.net',
                                                database='sql5521302',
                                                user='sql5521302',
                                                password='TvCHYlcKBJ'
                                          )
            if connection.is_connected():
                #print("MySQL connection is opened")
                cursor = connection.cursor()#
                cursor.execute(ssql)
                records = cursor.fetchall()
                #print(records)
                if len(records) > 0:
                  rv = True
                r = 'Executed : ' + ssql
                #print(r)
          except Error as e:
                r = "Error while executing : L"+ ssql + " ---- "
                print("Error while executing : L"+ ssql + " ---- ", e)
          finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    #print("MySQL connection is closed")
    return rv

def getquestionanswers(questionid, engine):
    rv = []
    questionid = questionid.strip().lower()
    engine = engine.strip().lower()
    if (len(questionid) > 0) & (len(engine) > 0):
          ssql = "SELECT answertitle, anwershort, answerlong FROM answers WHERE questionuniqueid='"+questionid.replace("'","''")+"' and engine='"+engine.replace("'","''")+"'"#
          try:
            connection = mysql.connector.connect(host='sql5.freemysqlhosting.net',
                                                database='sql5521302',
                                                user='sql5521302',
                                                password='TvCHYlcKBJ'
                                          )
            if connection.is_connected():
                #print("MySQL connection is opened")
                cursor = connection.cursor()#
                cursor.execute(ssql)
                records = cursor.fetchall()
                #print(records)
                if len(records) > 0:
                  rv = records
                r = 'Executed : ' + ssql
                #print(r)
          except Error as e:
                r = "Error while executing : L"+ ssql + " ---- "
                print("Error while executing : L"+ ssql + " ---- ", e)
          finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    #print("MySQL connection is closed")
    return rv

def askquestion(question, keywords, engine, waittime):
    rr = []
    qid = addquestion(question, engine, keywords)
    #print(qid)
    n = 0
    while (n < waittime) & (isquestionanswered(qid, engine) == False):
      n = n + 1
      #print(isquestionanswered(qid, 'a'))
      sleep(1)
    if isquestionanswered(qid, 'a'):
      print("########################################## question answered #################################################")
      a = getquestionanswers(qid, 'a')
      #print(a)
      rr = a
    return rr

def listentoquestions(howlong):
  i = 0
  while (i < howlong):
    i = i + 1
    #print('- ' + str(i)+ ' ------------------------------------')
    nextq = getfirstUnansweredQuestion('a')
    if len(nextq) > 0:
      qid = nextq[0]
      question = nextq[1]
      #print(question)
      r = answerthequestion_m(question)
      if len(r) > 0:
        ano = 0
        for r0 in r:
          #print(r0)
          ano = ano + 1
          try:
            x = addanswer(qid, r0[0],r0[1],r0[2],ano, 'a')
          except:
            pass
      x = markquestionasanswered(qid,'a')
    sleep(1)

def answerthequestion_m(question):
  r = []
  for i in range(0,2):
    r0 = [question + ' - Answer ' + str(i), question + ' - Answer ' + str(i), question + ' - Answer ' + str(i)]
    #print(r0)
    r.append(r0)
  return r

# adding a single-line text input widget
question = st.text_input('Enter your question: ', 'What are the challenges of oil-based growth?')
# displaying the entered text
ss= askquestion(question,'','a',60)
st.markdown("<b><font color=darkred>" + question + "</font><b>", unsafe_allow_html=True)
st.markdown("<font color=blue>Best possible answers based on the documents loaded (see more explanations by scrolling down):</font>", unsafe_allow_html=True)
#ss0 = ss[2]
for ss1 in ss[0][2].split('-@@-'):
   st.write(ss1)