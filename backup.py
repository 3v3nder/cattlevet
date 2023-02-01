from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://evender:Kachez#067@localhost/veterinary'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    code = db.Column(db.String(1000), nullable=False)



    def __repr__(self):
        return f'CareerCategories {self.name}'

class Symptoms(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    disease = db.Column(db.Integer(), db.ForeignKey(Disease.id))

    def __repr__(self):
        return f'EntryRequirements {self.name}'

"""
class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(10000), nullable=False)
    howToBecome = db.relationship('HowToBecome', backref='htb', lazy=True)
    dayToday = db.relationship('DaytoDayTasks', backref='dtd', lazy=True)
    whatItTakes = db.relationship('WhatItTakes', backref='wit', lazy=True)
    media = db.Column(db.String(1000), nullable=True)
    workPattern = db.Column(db.String(1000), nullable=False)
    hoursWorked = db.Column(db.String(1000), nullable=False)
    salaryStarter = db.Column(db.String(100), nullable=False)
    salaryExperienced = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    altnames = db.Column(db.String(1000), nullable=True)
    related = db.relationship('Related', backref='related', lazy=True)
    workenv = db.relationship('WorkingEnvironment', backref='workenv', lazy=True)
    careerpath = db.relationship('CareerPath', backref='careerpath', lazy=True)
    category = db.Column(db.Integer(), db.ForeignKey(CareerCategories.id))

    def __repr__(self):
        return f'Professional {self.name}'

class Related(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    profession = db.Column(db.Integer(), db.ForeignKey(Professional.id))

    def __repr__(self):
        return f'HowToBecome {self.name}'

class HowToBecome(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    requirements = db.relationship('EntryRequirements', backref='requirements', lazy=True)
    htbtypes = db.relationship('HTBtype', backref='HTBtype', lazy=True)
    profession = db.Column(db.Integer(), db.ForeignKey(Professional.id))

    def __repr__(self):
        return f'HowToBecome {self.name}'

class HTBtype(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    how2become = db.Column(db.Integer(), db.ForeignKey(HowToBecome.id))

    def __repr__(self):
        return f'EntryRequirements {self.name}'

class EntryRequirements(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    how2become = db.Column(db.Integer(), db.ForeignKey(HowToBecome.id))

    def __repr__(self):
        return f'EntryRequirements {self.name}'



class WhatItTakes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    profession = db.Column(db.Integer(), db.ForeignKey(Professional.id))

    def __repr__(self):
        return f'WhatItTakes {self.name}'

class DaytoDayTasks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    profession = db.Column(db.Integer(), db.ForeignKey(Professional.id))

    def __repr__(self):
        return f'DaytoDayTasks {self.name}'

class WorkingEnvironment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    profession = db.Column(db.Integer(), db.ForeignKey(Professional.id))

    def __repr__(self):
        return f'WorkingEnvironment {self.name}'

class CareerPath(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    profession = db.Column(db.Integer(), db.ForeignKey(Professional.id))

    def __repr__(self):
        return f'CareerPath {self.name}'






def careerCat(keyword):
    msg = CareerCategories.query.all()
    return msg


"""
@app.route("/test", methods=['GET', 'POST'])
def hello():

    if request.method == 'GET':

        r =requests.get('https://www.thecattlesite.com/diseaseinfo/')

        main = ('Welcome WE-NEXT AFRICA CHATBOT \n\n'
        'Below is our main menu NB: Click the links below each category or section to get access to that sections menu \n '
         '<li><a class="govuk-link" href="/job-categories/administration">Administration</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/animal-care">Animal care</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/beauty-and-wellbeing">Beauty and wellbeing</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/business-and-finance">Business and finance</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/computing-technology-and-digital">Computing, technology and digital</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/construction-and-trades">Construction and trades</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/creative-and-media">Creative and media</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/delivery-and-storage">Delivery and storage</a></li> \n'
                '<li><a class="govuk-link" href="/job-categories/emergency-and-uniform-services">Emergency and uniform services</a></li> \n'
        "3. *NewsHub* - To get access to local and international news headlines type newshub or click https://wa.me/+14155238886?text=newshub \n"
        "4. *Events and Updates* - To get access to WE-NEXT Africa's calendar of events and previous events videos that were also held type events and updates or click https://wa.me/+14155238886?text=events+and+updates \n")

        #msg = main.index("</li>", 1)
        #msg = main[165:177]
        jobCategories = []
        jobnameCategories = []
        #print(r)
        #print(r.text)
        msg = r.text
        #msg = main
        thecount = msg.count("option value=")
        msgstop = 1
        msgnamestop = 1
        
        for i in range(thecount):
            msgstart = msg.index("option value=", msgstop)
            msgstop = msg.index(">", msgstart)
            msgRealStart = msgstart + 14
            msgRealStop = msgstop - 1
            msgTitlenew = msg[msgRealStart:msgRealStop]
            #print(thecount)
            print(msgTitlenew)
            result = {"name" : msgnew}
            
            jobCategories.append(msgTitlenew)
            #print('https://www.thecattlesite.com/diseaseinfo/'+str(msgnew)+'/')

            

            r =requests.get('https://www.thecattlesite.com/diseaseinfo/'+str(msgTitlenew)+'/')

            msgdesc = r.text.lower()
            #msg = main
            msgdescstop = 1
            msgdescnamestop = 1
            if msgTitlenew != "187":

                if msgdesc.find("symptoms") != -1:
                    #print("there")

                    lastbound = msgdesc.index("<h3>", msgdesc.index("symptoms"))
                    #print(lastbound)

                    msgcheck = msgdesc.find("<li>", msgdesc.index("symptoms"), lastbound)
                    print(msgcheck)
                    if msgcheck != -1:
                        print(there)
                        msgdescnamestart = msgdesc.index("symptoms", msgdescnamestop)
                        print(msgdescnamestart)
                        msgdescnamestop = msgdesc.index("<h3>", msgdescnamestart)
                        print(msgdescnamestop)
                        msgdescRealStart = msgdescnamestart 
                        msgdescRealStop = msgdescnamestop 
                        msgnew1 = msgdesc[msgdescRealStart:msgdescRealStop]
                        print(msgnew1)
                        linkcount = msgnew1.count("<li>")
                        
                        msgdescriptionstop = msgdescnamestart

                        for i in range(linkcount):

                            msgdescriptionstart = msgdesc.index("<li>", msgdescriptionstop)
                            
                            msgdescriptionstop = msgdesc.index("</li>", msgdescriptionstart)
                            msgdescriptionRealStart = msgdescriptionstart + 4
                            msgdescriptionRealStop = msgdescriptionstop 
                            msgnew = msgdesc[msgdescriptionRealStart:msgdescriptionRealStop]

                            print(msgnew)

                            key = HowToBecome.query.filter_by(code = msgTitlenew).first()

                            job = Symptoms(name = msgnew, disease = key)
                            db.session.add(job)
                            db.session.commit()




            thedesccount = msgdesc.count("<h3>")
            print(thedesccount)
            if msgnew == "202":
                thedesccount = 0
            
            
            #SUB TITLE
            """
            for i in range(thedesccount):

                
                
                msgdescstart = msgdesc.index("<h3>", msgdescstop)
                
                msgdescstop = msgdesc.index("</h3>", msgdescstart)
                msgdescRealStart = msgdescstart + 4
                msgdescRealStop = msgdescstop 
                msgnew1 = msgdesc[msgdescRealStart:msgdescRealStop]
                print(msgnew1)
                #print(thecount)
                #print(msgnew)
                result = {"name" : msgnew1}

                thedescriptioncount = msgdesc.count("<p>")
                
                print(thedescriptioncount)
                if msgnew == "245":
                    thedescriptioncount = 0

                msgdescriptionstop = msgdescRealStop


                for i in range(thedescriptioncount):

                    
                    
                    msgdescriptionstart = msgdesc.index("<p>", msgdescriptionstop)
                    
                    msgdescriptionstop = msgdesc.index("</p>", msgdescriptionstart)
                    msgdescriptionRealStart = msgdescriptionstart + 4
                    msgdescriptionRealStop = msgdescriptionstop 
                    msgnew = msgdesc[msgdescriptionRealStart:msgdescriptionRealStop]
                    print(msgnew)
                    #print(thecount)
                    print(msgnew)
                    result = {"name" : msgnew}
            #print(jobCategories)
        
            
              job = CareerCategories(name = msgnew)
            db.session.add(job)
            db.session.commit()
        for i in reversed(jobCategories):
        #for i in jobCategories[jobCategories.index('environment-and-land'):]:
        #for i in jobCategories:
            print(i)
            #print('there')
            msgnew = i
            r =requests.get('https://nationalcareers.service.gov.uk/job-categories/'+ i)
            categ = r.text
            #print(categ)
            thecount = categ.count("/job-profiles/")
            #print(thecount)
            msgcategstop = 1
            for i in range(thecount):
                msgcategstart = categ.index("/job-profiles/", msgcategstop)
                msgcategstop = categ.index(">", msgcategstart)
                msgcategRealStart = msgcategstart + 14
                msgcategRealStop = msgcategstop - 1
                msgcategNamenew = categ[msgcategRealStart:msgcategRealStop]

                if msgcategNamenew.find("&#39;") != -1:
                    msgcategNamenew = msgcategNamenew.replace("&#39;", "'")
                print(msgcategNamenew)
                msgJobaltcheck = categ.index("</h2>", msgcategstart)
                #print(categ[msgJobaltcheck:msgJobaltcheck+50])
                #print(msgJobaltcheck)
                msgcheck = categ.find("<h3", msgJobaltcheck, msgJobaltcheck + 50)
                msgJobalt = ""
                #print(msgcheck)
                if msgcheck != -1:
                    msgcategstart = categ.index("jpAltTitle", msgcategstop)
                    msgcategstop = categ.index("</h3>", msgcategstart)
                    msgJobAltStart = msgcategstart + 12
                    msgJobAltStop = msgcategstop
                    msgJobalt = categ[msgJobAltStart:msgJobAltStop]
                    #print(msgJobalt)
                msgcategDescstart = categ.index("jpOverview", msgcategstop)
                msgcategDescstop = categ.index("</p>", msgcategDescstart)
                msgcategDescRealStart = msgcategDescstart + 12
                msgcategDescRealStop = msgcategDescstop - 1
                msgcategDescnew = categ[msgcategDescRealStart:msgcategDescRealStop]
                #print(msgcategDescnew)
                #Career Info
                msgcareerstarterstop = 1
                r = requests.get('https://nationalcareers.service.gov.uk/job-profiles/'+ msgcategNamenew)
                career = r.text

                startercheck = career.find("jpsstarter", msgcareerstarterstop)
                msgcareerstarterNamenew = ""
                msgcareerexperiencedNamenew = ""

                if startercheck != -1:

                    msgcareerstarterstart = career.index("jpsstarter", msgcareerstarterstop)
                    msgcareerstarterstop = career.index("<span>", msgcareerstarterstart)
                    msgcareerstarterRealStart = msgcareerstarterstart + 18
                    msgcareerstarterRealStop = msgcareerstarterstop - 1
                    msgcareerstarterNamenew = career[msgcareerstarterRealStart:msgcareerstarterRealStop]
                    #print(msgcareerstarterNamenew)
                    msgcareerexperiencedstop = 1
                    msgcareerexperiencedstart = career.index("jpsexperienced", msgcareerexperiencedstop)
                    msgcareerexperiencedstop = career.index("<span>", msgcareerexperiencedstart)
                    msgcareerexperiencedRealStart = msgcareerexperiencedstart + 22
                    msgcareerexperiencedRealStop = msgcareerexperiencedstop - 1
                    msgcareerexperiencedNamenew = career[msgcareerexperiencedRealStart:msgcareerexperiencedRealStop]
                    #print(msgcareerexperiencedNamenew)


                msgcareerweeklytimestop = 1
                msgcareerweeklytimestart = career.index("jphours", msgcareerweeklytimestop)
                msgcareerweeklytimestop = career.index("<span", msgcareerweeklytimestart)
                msgcareerweeklytimeRealStart = msgcareerweeklytimestart + 10
                msgcareerweeklytimeRealStop = msgcareerweeklytimestop - 1
                msgcareerweeklytimeNamenew = career[msgcareerweeklytimeRealStart:msgcareerweeklytimeRealStop]
                #print(msgcareerweeklytimeNamenew)




                msgcareerdailytimestop = 1
                check = career.find("jpwpattern", msgcareerdailytimestop)
                #print(check)
                msgcareerdailytimestart = career.index("jpwpattern", msgcareerdailytimestop)
                msgcareerdailytimestop = career.index("<span", msgcareerdailytimestart)
                msgcareerdailytimeRealStart = msgcareerdailytimestart + 13
                msgcareerdailytimeRealStop = msgcareerdailytimestop - 1
                msgcareerdailytimeNamenew = career[msgcareerdailytimeRealStart:msgcareerdailytimeRealStop]
                #print(msgcareerdailytimeNamenew)



                #How To Become

                msgcareerhowtobecomestop = 1
                msgcareerhowtobecomestart = career.index("job-profile-heading", msgcareerhowtobecomestop)
                msgcareerhowtobecomestop = career.index("<section", msgcareerhowtobecomestart)
                catype = career.count("<li>", msgcareerhowtobecomestart, msgcareerhowtobecomestop)
                #print(catype)
                msgcareerhowtobecomecatypestop = msgcareerhowtobecomestart
                howtobecomecatype = []
                for i in range(catype):
                    msgcareerhowtobecomecatypestart = career.index("<li>", msgcareerhowtobecomecatypestop)

                    msgcareerhowtobecomecatypestop = career.index("</li>", msgcareerhowtobecomecatypestart)
                    msgcareerhowtobecomecatypeRealStart = msgcareerhowtobecomecatypestart + 4
                    msgcareerhowtobecomecatypeRealStop = msgcareerhowtobecomecatypestop
                    msgcareerhowtobecomecatypeNamenew = career[msgcareerhowtobecomecatypeRealStart:msgcareerhowtobecomecatypeRealStop]
                    #print(msgcareerhowtobecomecatypeNamenew)
                    howtobecomecatype.append(msgcareerhowtobecomecatypeNamenew)
                    msgcareerhowtobecomesubsectionBoundarystop = msgcareerhowtobecomecatypestop

                if msgcategNamenew == "helicopter-engineer":
                    catype = 3

                msgcareerhowtobecomeh4Namenew = ""
                msgcareerhowtobecomepNamenew = ""
                howtobecomereqs = []
                howtobecomeneed = []
                for i in range(catype):
                    msgcareerhowtobecomesubsectionstart = career.index("job-profile-subsection-content", msgcareerhowtobecomesubsectionBoundarystop)
                    msgcareerhowtobecomesubsectionBoundarystop = career.index("</section>", msgcareerhowtobecomesubsectionstart)
                    msgcareerhowtobecomepstart = career.index("<p>", msgcareerhowtobecomesubsectionstart)
                    msgcareerhowtobecomepstop = career.index("</p>", msgcareerhowtobecomepstart)
                    msgcareerhowtobecomepRealStart = msgcareerhowtobecomepstart + 3
                    msgcareerhowtobecomepRealStop = msgcareerhowtobecomepstop - 1
                    msgcareerhowtobecomepNamenew = career[msgcareerhowtobecomepRealStart:msgcareerhowtobecomepRealStop]
                    howtobecomeneed.append(msgcareerhowtobecomepNamenew)
                    #print(msgcareerhowtobecomepNamenew)
                    h4check = career.find("<h4>", msgcareerhowtobecomesubsectionstart, msgcareerhowtobecomesubsectionBoundarystop)
                    #print(h4check)
                    msgcareerhowtobecomeneedstop = msgcareerhowtobecomepstop

                    if h4check != -1:
                        listcounttype = career.count("<li>", msgcareerhowtobecomepstart, h4check)


                        for i in range(listcounttype):
                            msgcareerhowtobecomeneedstart = career.index("<li>", msgcareerhowtobecomeneedstop)
                            msgcareerhowtobecomeneedstop = career.index("</li>", msgcareerhowtobecomeneedstart)
                            msgcareerhowtobecomeneedRealStart = msgcareerhowtobecomeneedstart + 4
                            msgcareerhowtobecomeneedRealStop = msgcareerhowtobecomeneedstop
                            msgcareerhowtobecomeneedNamenew = career[msgcareerhowtobecomeneedRealStart:msgcareerhowtobecomeneedRealStop]
                            #print(msgcareerhowtobecomeneedNamenew)
                            howtobecomeneed.append(msgcareerhowtobecomeneedNamenew)
                        msgcareerhowtobecomeh4start = career.index("<h4>", msgcareerhowtobecomeneedstop)
                        msgcareerhowtobecomeh4stop = career.index("</h4>", msgcareerhowtobecomeh4start)
                        msgcareerhowtobecomeh4RealStart = msgcareerhowtobecomeh4start + 4
                        msgcareerhowtobecomeh4RealStop = msgcareerhowtobecomeh4stop - 1
                        msgcareerhowtobecomeh4Namenew = career[msgcareerhowtobecomeh4RealStart:msgcareerhowtobecomeh4RealStop]
                        #print(msgcareerhowtobecomeh4Namenew)
                        msgcareerhowtobecomepstart = career.index("<p>", msgcareerhowtobecomeh4stop)
                        msgcareerhowtobecomepstop = career.index("</p>", msgcareerhowtobecomepstart)
                        msgcareerhowtobecomepRealStart = msgcareerhowtobecomepstart + 4
                        msgcareerhowtobecomepRealStop = msgcareerhowtobecomepstop
                        msgcareerhowtobecomepNamenew = career[msgcareerhowtobecomepRealStart:msgcareerhowtobecomepRealStop]
                        howtobecomereqs.append(msgcareerhowtobecomepNamenew)
                        #print(msgcareerhowtobecomepNamenew)
                        msgcareerhowtobecomereqsstop = msgcareerhowtobecomepstop

                        msgcareerhowtobecomeulcheckstart = career.index("</ul>", msgcareerhowtobecomeh4stop)
                        #print(msgcareerhowtobecomeulcheckstart)

                        listcount1type = career.count("<li>", msgcareerhowtobecomeh4start, msgcareerhowtobecomeulcheckstart)
                        #print(listcount1type)
                        for i in range(listcount1type):
                            msgcareerhowtobecomereqsstart = career.index("<li>", msgcareerhowtobecomereqsstop)
                            msgcareerhowtobecomereqsstop = career.index("</li>", msgcareerhowtobecomereqsstart)
                            msgcareerhowtobecomereqsRealStart = msgcareerhowtobecomereqsstart + 4
                            msgcareerhowtobecomereqsRealStop = msgcareerhowtobecomereqsstop - 1
                            msgcareerhowtobecomereqsNamenew = career[msgcareerhowtobecomereqsRealStart:msgcareerhowtobecomereqsRealStop]
                            #print(msgcareerhowtobecomereqsNamenew)
                            howtobecomereqs.append(msgcareerhowtobecomereqsNamenew)



                    else:
                        msgcareerhowtobecomeneedstart = career.index("<li>", msgcareerhowtobecomeneedstop)
                        msgcareerhowtobecomeneedstop = career.index("</li>", msgcareerhowtobecomeneedstart)
                        msgcareerhowtobecomeneedRealStart = msgcareerhowtobecomeneedstart + 4
                        msgcareerhowtobecomeneedRealStop = msgcareerhowtobecomeneedstop
                        msgcareerhowtobecomeneedNamenew = career[msgcareerhowtobecomeneedRealStart:msgcareerhowtobecomeneedRealStop]
                        #print(msgcareerhowtobecomeneedNamenew)
                        howtobecomeneed.append(msgcareerhowtobecomeneedNamenew)

                #What it takes

                msgcareerwhatittakesstop = 1
                msgcareerwhatittakesstart = career.index("Skills and knowledge", msgcareerwhatittakesstop)
                msgcareerwhatittakesstop = career.index("</section>", msgcareerwhatittakesstart)
                catype = career.count("<li>", msgcareerwhatittakesstart, msgcareerwhatittakesstop)
                #print(catype)
                msgcareerwhatittakescatypestop = msgcareerwhatittakesstart
                whatittakescatype = []
                for i in range(catype):
                    msgcareerwhatittakescatypestart = career.index("<li>", msgcareerwhatittakescatypestop)

                    msgcareerwhatittakescatypestop = career.index("</li>", msgcareerwhatittakescatypestart)
                    msgcareerwhatittakescatypeRealStart = msgcareerwhatittakescatypestart + 4
                    msgcareerwhatittakescatypeRealStop = msgcareerwhatittakescatypestop
                    msgcareerwhatittakescatypeNamenew = career[msgcareerwhatittakescatypeRealStart:msgcareerwhatittakescatypeRealStop]
                    #print(msgcareerwhatittakescatypeNamenew)
                    whatittakescatype.append(msgcareerwhatittakescatypeNamenew)


                #Day to Day tasks
                msgcareerdaytodaystop = 1
                msgcareerdaytodaystart = career.index("Day-to-day tasks", msgcareerdaytodaystop)
                msgcareerdaytodaystop = career.index("</section>", msgcareerdaytodaystart)
                catype = career.count("<li>", msgcareerdaytodaystart, msgcareerdaytodaystop)
                #print(catype)
                msgcareerdaytodaycatypestop = msgcareerdaytodaystart
                daytodaycatype = []
                for i in range(catype):
                    msgcareerdaytodaycatypestart = career.index("<li>", msgcareerdaytodaycatypestop)

                    msgcareerdaytodaycatypestop = career.index("</li>", msgcareerdaytodaycatypestart)
                    msgcareerdaytodaycatypeRealStart = msgcareerdaytodaycatypestart + 4
                    msgcareerdaytodaycatypeRealStop = msgcareerdaytodaycatypestop
                    msgcareerdaytodaycatypeNamenew = career[msgcareerdaytodaycatypeRealStart:msgcareerdaytodaycatypeRealStop]
                    #print(msgcareerdaytodaycatypeNamenew)
                    daytodaycatype.append(msgcareerdaytodaycatypeNamenew)

                msgcareerdaytodayenvironmentstop = 1
                msgcareerdaytodayenvironmentstart = career.index("Working environment", msgcareerdaytodayenvironmentstop)
                msgcareerdaytodayenvironmentstop = career.index("</section>", msgcareerdaytodayenvironmentstart)
                catype = career.count("<p>", msgcareerdaytodayenvironmentstart, msgcareerdaytodayenvironmentstop)
                #print(catype)
                msgcareerdaytodayenvironmentcatypestop = msgcareerdaytodayenvironmentstart
                daytodayenvironmentcatype = []
                for i in range(catype):
                    msgcareerdaytodayenvironmentcatypestart = career.index("<p>", msgcareerdaytodayenvironmentcatypestop)

                    msgcareerdaytodayenvironmentcatypestop = career.index("</p>", msgcareerdaytodayenvironmentcatypestart)
                    msgcareerdaytodayenvironmentcatypeRealStart = msgcareerdaytodayenvironmentcatypestart + 3
                    msgcareerdaytodayenvironmentcatypeRealStop = msgcareerdaytodayenvironmentcatypestop
                    msgcareerdaytodayenvironmentcatypeNamenew = career[msgcareerdaytodayenvironmentcatypeRealStart:msgcareerdaytodayenvironmentcatypeRealStop]
                    #print(msgcareerdaytodayenvironmentcatypeNamenew)
                    daytodayenvironmentcatype.append(msgcareerdaytodayenvironmentcatypeNamenew)

                #Career path and progressions
                msgcareerpathandprogressstop = 1
                msgcareerpathandprogressstart = career.index("Career path and progression", msgcareerpathandprogressstop)
                msgcareerpathandprogressstop = career.index("</section>", msgcareerpathandprogressstart)
                catype = career.count("<li>", msgcareerpathandprogressstart, msgcareerpathandprogressstop)
                #print(catype)
                msgcareerpathandprogresscatypestop = msgcareerpathandprogressstart
                pathandprogresscatype = []
                for i in range(catype):
                    msgcareerpathandprogresscatypestart = career.index("<li>", msgcareerpathandprogresscatypestop)

                    msgcareerpathandprogresscatypestop = career.index("</li>", msgcareerpathandprogresscatypestart)
                    msgcareerpathandprogresscatypeRealStart = msgcareerpathandprogresscatypestart + 4
                    msgcareerpathandprogresscatypeRealStop = msgcareerpathandprogresscatypestop
                    msgcareerpathandprogresscatypeNamenew = career[msgcareerpathandprogresscatypeRealStart:msgcareerpathandprogresscatypeRealStop]
                    #print(msgcareerpathandprogresscatypeNamenew)
                    pathandprogresscatype.append(msgcareerpathandprogresscatypeNamenew)

                msgcareerpathandprogressstop = 1
                msgcareerpathandprogressstart = career.index("CareerPathAndProgression", msgcareerpathandprogressstop)
                msgcareerpathandprogressstop = career.index("</section>", msgcareerpathandprogressstart)
                catype = career.count("<p>", msgcareerpathandprogressstart, msgcareerpathandprogressstop)
                #print(catype)
                msgcareerpathandprogresscatypestop = msgcareerpathandprogressstart
                pathandprogresscatype = []
                for i in range(catype):
                    msgcareerpathandprogresscatypestart = career.index("<p>", msgcareerpathandprogresscatypestop)

                    msgcareerpathandprogresscatypestop = career.index("</p>", msgcareerpathandprogresscatypestart)
                    msgcareerpathandprogresscatypeRealStart = msgcareerpathandprogresscatypestart + 3
                    msgcareerpathandprogresscatypeRealStop = msgcareerpathandprogresscatypestop
                    msgcareerpathandprogresscatypeNamenew = career[msgcareerpathandprogresscatypeRealStart:msgcareerpathandprogresscatypeRealStop]
                    #print(msgcareerpathandprogresscatypeNamenew)
                    pathandprogresscatype.append(msgcareerpathandprogresscatypeNamenew)

                #Related Careers

                msgcareerrelatedcareersstop = 1
                msgcareerrelatedcareersstart = career.index("Related careers", msgcareerrelatedcareersstop)
                msgcareerrelatedcareersstop = career.index("</div>", msgcareerrelatedcareersstart)
                catype = career.count("/job-profiles/", msgcareerrelatedcareersstart, msgcareerrelatedcareersstop)
                #print(catype)
                msgcareerrelatedcareerscatypestop = msgcareerrelatedcareersstart
                relatedcareerscaptype = []
                for i in range(catype):
                    msgcareerrelatedcareerscatypestart = career.index("/job-profiles/", msgcareerrelatedcareerscatypestop)

                    msgcareerrelatedcareerscatypestop = career.index(">", msgcareerrelatedcareerscatypestart)
                    msgcareerrelatedcareerscatypeRealStart = msgcareerrelatedcareerscatypestart + 14
                    msgcareerrelatedcareerscatypeRealStop = msgcareerrelatedcareerscatypestop - 1
                    msgcareerrelatedcareerscatypeNamenew = career[msgcareerrelatedcareerscatypeRealStart:msgcareerrelatedcareerscatypeRealStop]
                    #print(msgcareerrelatedcareerscatypeNamenew)
                    relatedcareerscaptype.append(msgcareerrelatedcareerscatypeNamenew)

                cati= CareerCategories.query.filter_by(name = msgnew).first()

                job = Professional(name = msgcategNamenew, altnames = msgJobalt,  hoursWorked = msgcareerweeklytimeNamenew, workPattern = msgcareerdailytimeNamenew, salaryStarter = msgcareerstarterNamenew, salaryExperienced =  msgcareerexperiencedNamenew, description = msgcategDescnew, category = cati.id)
                db.session.add(job)
                #result = {"name" : msgcategNamenew, "altnames" : msgJobalt,  "hoursWorked" : msgcareerweeklytimeNamenew, "workPattern" : msgcareerdailytimeNamenew, "salaryStarter" : msgcareerstarterNamenew, "salaryExperienced" :  msgcareerexperiencedNamenew, "description" : msgcategDescnew, "category" : cati.id}
                #requests.post('https://tatz.pythonanywhere.com/proff', json=result)
                categi = Professional.query.filter_by(name = msgcategNamenew).first()

                for i in daytodaycatype:
                    jobdaytoday = DaytoDayTasks(name = i, profession = categi.id)
                    result = {"name" : i, "profession" : categi.id}
                    #requests.post('https://tatz.pythonanywhere.com/day2day', json=result)
                    #db.session.add(jobdaytoday)

                for i in daytodayenvironmentcatype:
                    jobenvironmentcatype = WorkingEnvironment(name = i, profession = categi.id)
                    result = {"name" : i, "profession" : categi.id}
                    #requests.post('https://tatz.pythonanywhere.com/daytodayenvironment', json=result)
                    db.session.add(jobenvironmentcatype)

                for i in whatittakescatype:
                    i = i.replace("  ", "")
                    jobwhatittakes = WhatItTakes(name = i, profession = categi.id)
                    result = {"name" : i, "profession" : categi.id}
                    #requests.post('https://tatz.pythonanywhere.com/whatittakes', json=result)
                    db.session.add(jobwhatittakes)

                for i in pathandprogresscatype:
                    jobpathandprogress = CareerPath(name = i, profession = categi.id)
                    result = {"name" : i, "profession" : categi.id}
                    #requests.post('https://tatz.pythonanywhere.com/pathandprogress', json=result)
                    db.session.add(jobpathandprogress)

                for i in relatedcareerscaptype:
                    jobrelatedcareers = Related(name = i, profession = categi.id)
                    result = {"name" : i, "profession" : categi.id}
                    #requests.post('https://tatz.pythonanywhere.com/relatedcareers', json=result)
                    #db.session.add(jobrelatedcareers)

                for i in howtobecomecatype:

                    jobhowtobecome = HowToBecome(name = i, profession = categi.id)
                    result = {"name" : i, "profession" : categi.id}
                    #requests.post('https://tatz.pythonanywhere.com/howtobecome', json=result)
                    db.session.add(jobhowtobecome)
                    htbtpe = HowToBecome.query.filter_by(profession = categi.id, name = i).first()
                    #print(htbtpe)
                    #print(htbtpe.id)


                    for i in howtobecomeneed:
                        i = i.replace("  ", "")
                        jobhowtobecomeneed = HTBtype(name = i, how2become = htbtpe.id)
                        result = {"name" : i, "how2become" : htbtpe.id}
                        requests.post('https://tatz.pythonanywhere.com/howtobecomeneed', json=result)
                        db.session.add(jobhowtobecomeneed)

                        htbtpereq = HTBtype.query.filter_by(name = i, how2become=htbtpe.id).first()
                        #print(htbtpereq)



                        for i in howtobecomereqs:
                            jobhowtobecomeneedreqs = EntryRequirements(name = i, how2becomeType = htbtpereq.id)
                            result = {"name" : i, "how2becomeType" : htbtpereq.id}
                            #requests.post('https://tatz.pythonanywhere.com/howtobecomeneedreqs', json=result)
                            db.session.add(jobhowtobecomeneedreqs)

                #db.session.commit()
"""













        return str(jobCategories)

@app.route("/proff", methods=['GET', 'POST'])
def proff():
    if request.method == 'POST':
        proff = request.json
        job = Professional(name = proff['name'], altnames = proff['altnames'],  hoursWorked = proff['hoursWorked'], workPattern = proff['workPattern'], salaryStarter = proff['salaryStarter'], salaryExperienced =  proff['salaryExperienced'], description = proff['description'], category = proff['category'])
        db.session.add(job)
        db.session.commit()
        return("good")

    return render_template('sms.html')

@app.route("/day2day", methods=['GET', 'POST'])
def day2day():
    if request.method == 'POST':
        jobdaytoday = request.json
        jobdaytoday = DaytoDayTasks(name = jobdaytoday['name'], profession = jobdaytoday['profession'])
        db.session.add(jobdaytoday)
        db.session.commit()
        return("good")

    return render_template('sms.html')

@app.route("/whatittakes", methods=['GET', 'POST'])
def whatittakes():
    if request.method == 'POST':
        jobwhatittakes = request.json
        jobwhatittakes = WhatItTakes(name = jobwhatittakes['name'], profession = jobwhatittakes['profession'])
        db.session.add(jobwhatittakes)
        db.session.commit()
        return("true")

@app.route("/daytodayenvironment", methods=['GET', 'POST'])
def daytodayenvironment():
    if request.method == 'POST':
        jobenvironmentcatype = request.json
        jobenvironmentcatype = WorkingEnvironment(name = jobenvironmentcatype['name'], profession = jobenvironmentcatype['profession'])
        db.session.add(jobenvironmentcatype)
        db.session.commit()
        return("good")

@app.route("/pathandprogress", methods=['GET', 'POST'])
def pathandprogress():
    if request.method == 'POST':
        jobpathandprogress = request.json
        jobpathandprogress = CareerPath(name = jobpathandprogress['name'], profession = jobpathandprogress['profession'])
        db.session.add(jobpathandprogress)
        db.session.commit()
        return("good")


@app.route("/relatedcareers", methods=['GET', 'POST'])
def relatedcareers():
    if request.method == 'POST':
        jobrelatedcareers = request.json
        jobrelatedcareers = Related(name = jobrelatedcareers['name'], profession = jobrelatedcareers['profession'])
        db.session.add(jobrelatedcareers)
        db.session.commit()
        print("good")
        return("good")

@app.route("/howtobecome", methods=['GET', 'POST'])
def howtobecome():
    if request.method == 'POST':
        jobhowtobecome = request.json
        jobhowtobecome = HowToBecome(name = jobhowtobecome['name'], profession = jobhowtobecome['profession'])
        db.session.add(jobhowtobecome)
        db.session.commit()
        return("good")

@app.route("/howtobecomeneed", methods=['GET', 'POST'])
def howtobecomeneed():
    if request.method == 'POST':
        jobhowtobecomeneed = request.json
        jobhowtobecomeneed = HTBtype(name = jobhowtobecomeneed['name'], how2become = jobhowtobecomeneed['how2become'])
        db.session.add(jobhowtobecomeneed)
        db.session.commit()
        return("good")

@app.route("/howtobecomeneedreqs", methods=['GET', 'POST'])
def howtobecomeneedreqs():
    if request.method == 'POST':
        jobhowtobecomeneedreqs = request.json
        jobhowtobecomeneedreqs = EntryRequirements(name = jobhowtobecomeneedreqs['name'], how2become = jobhowtobecomeneedreqs['how2become'])
        db.session.add(jobhowtobecomeneedreqs)
        db.session.commit()
        return("good")

"""
@app.route("/")
def hello():
    r =requests.get('https://nationalcareers.service.gov.uk/explore-careers')

    main = ('Welcome WE-NEXT AFRICA CHATBOT \n\n'
    'Below is our main menu NB: Click the links below each category or section to get access to that sections menu \n '
     '<li><a class="govuk-link" href="/job-categories/administration">Administration</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/animal-care">Animal care</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/beauty-and-wellbeing">Beauty and wellbeing</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/business-and-finance">Business and finance</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/computing-technology-and-digital">Computing, technology and digital</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/construction-and-trades">Construction and trades</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/creative-and-media">Creative and media</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/delivery-and-storage">Delivery and storage</a></li> \n'
            '<li><a class="govuk-link" href="/job-categories/emergency-and-uniform-services">Emergency and uniform services</a></li> \n'
    "3. *NewsHub* - To get access to local and international news headlines type newshub or click https://wa.me/+14155238886?text=newshub \n"
    "4. *Events and Updates* - To get access to WE-NEXT Africa's calendar of events and previous events videos that were also held type events and updates or click https://wa.me/+14155238886?text=events+and+updates \n")

    #msg = main.index("</li>", 1)
    #msg = main[165:177]
    jobCategories = []
    print(r)
    print(r.text)
    msg = r.text
    #msg = main
    thecount = msg.count("/job-categories/")
    msgstop = 1
    for i in range(thecount):
        msgstart = msg.index("/job-categories/", msgstop)
        msgstop = msg.index(">", msgstart)
        msgRealStart = msgstart + 16
        msgRealStop = msgstop - 1
        msgnew = msg[msgRealStart:msgRealStop]
        print(thecount)
        print(msgnew)
        jobCategories.append(msgnew)
        msg.replace("/job-categories/", " ", 1)
        i += 2
    for i in jobCategories:
        jobcat = CategoriesInternal(name = i)
        db.session.add(job)
        db.session.commit()


    return str(jobCategories)

    """

"""
@app.route("adding")
def adding():
    post = CareerCategories(, name=name,)
    db.session.add(post)
    db.session.commit()
    """

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    if request.method == 'POST':
    #fetch the message
        msg = request.form.get('Body').lower()
        number = request.values.get('From', '')
        #msg = request.form['username'].lower()
        #msg = request.form['username']
        client = Client("ACe5b4d5166816d11c745a003dd9a282b6", "465b82682ecd99f731c3fa656c49bd2f")
        print(msg)
        resp = MessagingResponse()

        #message = resp.message()
        """
        for i in range(0, len(msg), 1):
                if (msg[i] == '_'):
                    msg = msg.replace(msg[i], ' ')
                    """


        main = ("Welcome WE-NEXT AFRICA CHATBOT \n\n"
        "Below is our main menu NB: Click the links below each category or section to get access to that section's menu \n\n "
        "1. *Career Info* - To get access to our proffessional information type CareerGuide or click https://wa.me/+14155238886?text=CareerGuide\n\n "
        "2. *Library* - To get access to elearning materials, educational resources  subjects, topics, marking schemes, syllabus material, past papers,"
        "notes, and journals type e-lib or click https://wa.me/+14155238886?text=e-lib\n\n"
        "3. *NewsHub* - To get access to local and international news headlines type newshub or click https://wa.me/+14155238886?text=newshub \n\n"
        "4. *Events and Updates* - To get access to WE-NEXT Africa's calendar of events and previous events videos that were also held type events and updates or click https://wa.me/+14155238886?text=events+and+updates \n\n")



        Science= ("Welcome to the keyword section \n\n"
            "*Career Info* allows users to get access to our proffessionals information\n"
            "The careers in keyword are shown in the menu is listed below:\n\n"
            "1. Science and Technology type science and tech or click https://wa.me/+14155238886?text=science+and+tech\n"
            "2. Social Sciences type social sciences or click https://wa.me/+14155238886?text=social+sciences\n"
            "3. Commerce type commerce or click https://wa.me/+14155238886?text=commerce\n"
            "4. Arts type arts or click https://wa.me/+14155238886?text=arts\n"
            )
        library= ("Welcome to the *Library* section \n\n"
            "The *Library* allows users to get access to elearning materials, educational resources  subjects, topics, marking schemes, syllabus material, past papers,"
        "notes, and journals\n"
            " The *Library* menu is listed below:\n\n"
            "")
        career= ("Welcome to the *NewsHub* section \n\n"
            "*NewsHub* allows users to get access to local and international news headlines type newshub\n"
            "The *NewsHub* menu is listed below:\n\n"
            )
        career= ("Welcome to the *Events and Updates* section \n\n"
            "*Events and Updates* allows users to get access to WE-NEXT Africa's calendar of events and previous events videos that were also held\n"
            "The *Events and Updates* menu is listed below:\n\n")
        """
        messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to="whatsapp:+263784873574",
                body=main,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
                )
                """



        #print(message.sid)

        if msg == "sports":

            resp.message(sports)
            #resp1.media("https://demo.twilio.com/owl.png")
            #message.body(sports)
        careerg = "careerguide"

        if str(msg) == "hi":
            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=main,)


        careergCount = 0
        offset =  12
        if "categ" in str(msg):
            offset =  5

        if "careersearch" in str(msg):
            offset =  5

        digits = []
        digitReal = []





        if "careergcountplus" in str(msg):
            cahr = msg[msg.index("careergcountplus"):]
            for character in cahr:
                if character.isdigit():
                    digindex = msg.index(character)
                    digits.append(digindex)

            for d in digits:
                digitReal.append(msg[d])

            dig = ""

            for d in digitReal:
                dig += d

            careergCount = int(dig)
            careergCount = careergCount + 1
            msg = msg[:msg.index("careergcountplus")]

        careergCountoffset = offset * careergCount

        search = []


        if "careersearch=" in str(msg):
            categ1 = Professional.query.all()
            msg = msg[13:]
            print(msg)
            for cat in categ1:
                if msg in cat.name:
                    search.append(cat.id)

            if search == []:
                cat = "Results not found \n\n"
            else:

                cat = "Here are the results \n\n"


                for index, res in enumerate(search[careergCountoffset:]):
                    prof = Professional.query.filter_by(id=res).first()

                    catsingle = "*"+prof.name.title()+ "* \n AKA:"+ prof.altnames.title() + "\n"+ prof.description+ "\n" "Type proff=" +str(prof.id)+ " or click https://wa.me/+14155238886?text=proff="+str(prof.id)+"\n\n"
                    cat = cat + catsingle
                    if  index == offset:
                        break


                careersinglenew = "To view more click: https://wa.me/+14155238886?text=careersearch="+str(msg)+"careergcountplus"+str(careergCount)+"\n"
                cat = cat + careersinglenew
                    #print(categ)
                    #print(cat)

            messages = client.messages.create(
                        from_="whatsapp:+14155238886",
                        to=number,
                        body=cat,
                        media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
                    )


        if str(msg) == careerg:
            print('there')
            categories = CareerCategories.query.limit(12).offset(careergCountoffset).all()
            careerType= "Welcome to the Career Info section \n\n *Career Info* allows users to get access to our proffessionals information\n\n To perform a search type careersearch={keyword}, for example careersearch=nurse or click:\n https://wa.me/+14155238886?text=careersearch=\n\n"
            "Select the category of the career you want to research about on the menu is listed below:\n\n"
            for category in categories:
                careersingle = str(category.id) + ".*" +category.name.title()+ "* Type categ="+str(category.id)+ " or click https://wa.me/+14155238886?text=categ="+str(category.id)+"\n\n"
                careerType = careerType + str(careersingle)
            careersinglenew = "To view more click: https://wa.me/+14155238886?text=careerguidecareergcountplus"+str(careergCount)+"\n"
            careerType = careerType + careersinglenew
            print(categories)
            print(careerType)
            resp.message(careerType)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=careerType,)

            return messages
            #return careerType

        print("categ" in str(msg))
        if "categ" in str(msg):
            msg = str(msg).replace('categ=', '')
            print(msg)
            categ = Professional.query.filter_by(category=msg).limit(5).offset(careergCountoffset).all()
            msg = CareerCategories.query.filter_by(id=msg).first()



            cat = "Welcome to the *" +str(msg.name).title()+ "* section \n\n"
            "Select the profession in "+ str(msg.name).title()+  "you want to research about on the menu is listed below:\n\n"
            for prof in categ:
                catsingle = "*"+prof.name.title()+ "* \n AKA:"+ prof.altnames.title() + "\n"+ prof.description+ "\n" "Type proff=" +str(prof.id)+ " or click https://wa.me/+14155238886?text=proff="+str(prof.id)+"\n\n"
                cat = cat + catsingle

            careersinglenew = "To view more click: https://wa.me/+14155238886?text=categ="+str(msg.id)+"careergcountplus"+str(careergCount)+"\n"
            cat = cat + careersinglenew
            #print(categ)
            #print(cat)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
               )
            #return str(cat)
            #resp.message(cat)
        if "proff" in str(msg):

            msg = str(msg).replace('proff=', '')
            print(msg)
            categ = Professional.query.filter_by(id=msg).first()
            related = Related.query.filter_by(profession=msg).limit(3).all()
            print(categ.description)
            cat = "*"+categ.name.title()+ "* \n\n Other names: "+ categ.altnames.title() + "\n\n"+ categ.description+ "\n\n" "Average Starter salary:"+ categ.salaryStarter+ "\n" "Average Experienced salary:"+ categ.salaryExperienced+ "\n\n"
            cat2 =" Type proff=" +str(categ.id)+ " or click https://wa.me/+14155238886?text=H2B="+str(categ.id)+" to view How To Become a "+ categ.name+ "\n\n"
            cat3 = " Type proff=" +str(categ.id)+ " or click https://wa.me/+14155238886?text=D2D="+str(categ.id)+" to view The Day to Day Tasks \n\n"
            cat4 =" Type proff=" +str(categ.id)+ " or click https://wa.me/+14155238886?text=WIT="+str(categ.id)+" to view The Day to Day Tasks \n\n"
            cat6 = " Type proff=" +str(categ.id)+ " or click https://wa.me/+14155238886?text=CarrPath="+str(categ.id)+" to view The Career Path \n\n Related Careers:\n"
            cat = cat + cat2+ cat3 + cat4+ cat6
            for prof in related:
                categ = Professional.query.filter_by(name=prof.name).first()
                catsingle = "*"+prof.name.title()+ "* \n\n Type proff=" +str(categ.id)+ " or click https://wa.me/+14155238886?text=proff="+str(categ.id)+"\n To view *"+ prof.name.title() + "* \n\n"
                cat = cat + catsingle

            """
            cat = categ.name+ "\n\n"

            "Definition:" "\n"
            +categ.description+ "How to become:\n\n""+ categ.howToBecome + type profession=categ.name" "or click https://wa.me/+14155238886?text=categ=""\n"
                """

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=[categ.media],
               )
            print(categ)
            print(cat)
            #return str(cat)
            resp.message(cat)

        if "d2d" in str(msg):
            msg = str(msg).replace('d2d=', '')
            print(msg)
            daytoday = DaytoDayTasks.query.filter_by(profession=msg).all()
            msg = Professional.query.filter_by(id=msg).first()



            cat = "Welcome to the *" +str(msg.name).title()+ "* section \n\n"
            "Day To Day Tasks:\n\n"
            for prof in daytoday:
                catsingle =prof.name.title()+ "\n\n"
                cat = cat + catsingle

            #print(categ)
            #print(cat)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
               )
            #return str(cat)
            #resp.message(cat)

        if "wit" in str(msg):
            msg = str(msg).replace('wit=', '')
            print(msg)
            whatittakes = WhatItTakes.query.filter_by(profession=msg).all()
            env = WorkingEnvironment.query.filter_by(profession=msg).all()
            msg = Professional.query.filter_by(id=msg).first()





            cat = "Welcome to the *" +str(msg.name).title()+ "* section \n\n What it takes:\n\n"

            for prof in whatittakes:
                prof.name = str(prof.name).replace('  ', '')
                catsingle = prof.name+ "\n"
                cat = cat + catsingle
            work = "Working Environment: \n\n"
            cat = cat + work
            for prof in env:
                prof.name = prof.name.replace('  ', '')
                catsingle =prof.name.title()+ "\n\n"
                cat = cat + catsingle


            #print(categ)
            #print(cat)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
               )
            #return str(cat)
            #resp.message(cat)

        if "carrpath" in str(msg):
            msg = str(msg).replace('carrpath=', '')
            print(msg)
            carrerPath = CareerPath.query.filter_by(profession=msg).all()
            msg = Professional.query.filter_by(id=msg).first()




            cat = "Welcome to the" +str(msg.name).title()+ " section \n\n"
            "Career Path:\n\n"
            for prof in carrerPath:
                cat = str(prof.id) + ")"+prof.name.title()+ "\n"


            #print(categ)
            #print(cat)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
               )
            #return str(cat)
            #resp.message(cat)

        if "h2b" in str(msg):
            msg = str(msg).replace('h2b=', '')
            print(msg)
            h2b = HowToBecome.query.filter_by(profession=msg).all()
            msg = Professional.query.filter_by(id=msg).first()




            cat = "Welcome to the *" +str(msg.name).title()+ "* needs section \n\n"
            for prof in h2b:
                catsingle = "*"+prof.name.title()+ "* Type htbneed=" +str(prof.id)+ " or click https://wa.me/+14155238886?text=Htbneed="+str(prof.id)+" to view "+ prof.name+ "\n\n"

                cat = cat + catsingle
                #h2bneed = HTBtype.query.filter_by(how2become=prof.id).all()
                #for pro in h2bneed:
                #    catsingle = str(pro.id) + ")"+pro.name.title()+ "\n\n"
                #    cat = cat + catsingle



            #print(categ)
            #print(cat)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
               )
            #return str(cat)
            #resp.message(cat)

        if "htbneed" in str(msg):
            msg = str(msg).replace('htbneed=', '')
            print(msg)
            h2bneed = HTBtype.query.filter_by(how2become=msg).all()
            msg = HowToBecome.query.filter_by(id=msg).first()
            reqs = EntryRequirements.query.filter_by(how2become=msg).all()




            cat = "This is how you can get involved in the career through *" +str(msg.name).title()+ "*: \n\n"
            for pro in h2bneed:
                catsingle = pro.name.title()+ "\n\n"

                cat = cat + catsingle

            catsinglenew = "Requirements: \n\n"
            cat = cat + catsinglenew

            for pro in reqs:
                catsingle = pro.name.title()+ "\n\n"

                cat = cat + catsingle




            #print(categ)
            #print(cat)

            messages = client.messages.create(
                from_="whatsapp:+14155238886",
                to=number,
                body=cat,
                media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
               )
            #return str(cat)
            #resp.message(cat)

        if msg =="science and tech":
            categ = CareerCategories.query.filter_by(professions=msg)
            catprofessions = categ.professions

            cat = ("Welcome to the",msg, " section \n\n"
            "*",msg,"* definition\n"
            "Select the profession in ", msg,  "you want to research about on the menu is listed below:\n\n")
            for prof in catprofessions:
                cat = cat+ (prof.id, ".", prof, " type profession=",prof, "or click https://wa.me/+14155238886?text=",prof.id,prof.name,"\n")
            resp.message(cat)
        """if msg =="library":
            return
        if msg =="events and updates":
            return
        if msg =="newshub":
            return
            """


        #Create reply
        #resp = MessagingResponse()
        #resp.message("You said: {}".format(msg))dsdsdsdsds
        #print(cat)

        return str(resp)
    else:
        return render_template('sms.html')

if __name__ == "__main__":
    app.run(debug=True)

