#!/usr/bin/python
from PyQt4 import QtCore, QtSql, QtGui

import pandas as pd
import numpy as np

from table_view import Ui_MainWindow

class Yahoo(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Yahoo, self).__init__()
    
        self.move(300,300)
        self.setWindowTitle("Sql browser")
        
        self.createConnection()
        self.createModel()
        self.initUI()
        
        self.statusBar().showMessage("Ready")
        
        #self.printData(query)
        
    def printData(self, query):
        
        pass
        
        
    
    
    
        
    def onClicked(self, index):
        self.statusBar().showMessage(index.data().toString())
        
    def createConnection(self):
        
        #self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        #self.db.setDatabaseName("friends.db")
        
        self.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        self.db.setHostName("cit.tesla.local")
        self.db.setDatabaseName("cit2")
        self.db.setUserName("python")
        self.db.setPassword("python")
      
        
        
        if not self.db.open():
            print ("cannot establish a database connection", self.db.lastError().text())
            return False
        
    def createModel(self):
        
        self.model = QtSql.QSqlQueryModel()
        
        query = QtSql.QSqlQuery(self.db)
        
    def runQuery(self):
        
        #query.exec_("select * from generated_reports")
        #query.exec_("SELECT * FROM `work_logs` WHERE `duration` > 4000")
        #query.exec_("SELECT *  FROM `work_logs` WHERE `company_id` = 54132 AND `customer_id` = 104147 AND `started_at` \
        #                          > '2014-08-01 10:48:02' AND `duration` > 40 \
         #                         ORDER BY `work_logs`.`log_type` ASC")
        #query.exec_("select * from Friends")
        #query.exec_("select * from Friends")
        #query.exec_("SELECT `task_id`,`project_id`,`customer_id`,`started_at`, `duration` FROM `work_logs` WHERE `company_id` =54132 AND `customer_id` =104147 \
                    #AND `started_at` > '2014-08-01 10:48:02'")
                    
        sql="SELECT `projects`.`name`,`work_logs`.`task_id`,`tasks`.`name`  ,(SUM( `work_logs`.`duration` )/3600) \
        as Total FROM `work_logs` INNER JOIN `tasks` on tasks.id = work_logs.task_id INNER JOIN `projects` on projects.id = work_logs.project_id \
        WHERE DATE_ADD(`work_logs`.`started_at`,INTERVAL 1 DAY) > '2014-08-01 00:00:00' AND `work_logs`.`user_id`=116196 GROUP BY `tasks`.`name` ORDER BY `projects`.`name` ASC"        
        
        #sql="SELECT `projects`.`name`,`work_logs`.`task_id`,`tasks`.`name`  ,(SUM( `work_logs`.`duration` ) /3600) \
        #as Total FROM `work_logs` INNER JOIN `tasks` on tasks.id = work_logs.task_id INNER JOIN `projects` on projects.id = work_logs.project_id \
        #WHERE `work_logs`.`started_at`> '2014-08-01 00:00:00' AND `work_logs`.`user_id`=116196 GROUP BY `tasks`.`name` ORDER BY `projects`.`name` ASC"           
        
        
        query.exec_(sql)        
        
        
        
        
        #self.model.removeColumn(0)
        
        #self.model.setHeaderData(0, QtCore.Qt.Horizontal,QtCore.QVariant("Name")) # these only rename the header.
        #self.model.setHeaderData(1, QtCore.Qt.Horizontal,QtCore.QVariant("Age"))
        
        DATETIME_FORMAT = "yyyy-MM-dd hh:mm:ss"
        PROJECTNAME, TASKID, TASKNAME, DURATION, STARTEDAT = range(5)        
        
        while query.next():
            projectname=unicode(query.value(PROJECTNAME).toString())
            taskid=query.value(TASKID).toInt()[0]
            taskname=unicode(query.value(TASKNAME).toString())
            duration=query.value(DURATION).toFloat()[0]
            
            
            #print projectname, taskid, taskname, duration
            
           
        query2 = QtSql.QSqlQuery(self.db)
        
                    
   
        
        query2.exec_("SELECT `projects`.`name` as 'Project name' ,`work_logs`.`task_id`,`tasks`.`name` as 'Task Name'  , (`work_logs`.`duration`)/3600 as Total , DAY(DATE_ADD(`work_logs`.`started_at`, INTERVAL 12 HOUR)) AS 'DAY' FROM `work_logs` \
        INNER JOIN `tasks` on tasks.id = work_logs.task_id \
        INNER JOIN `projects` on projects.id = work_logs.project_id \
        WHERE `work_logs`.`started_at` > '2014-08-01 00:00:00' AND `work_logs`.`user_id`=116196 ")       
        
        #print 'passing through'

        taskidsL=[]
        tasknameL=[]
        durationL=[]
        started_at2L=[]
        projectnameL=[]

        while query2.next():
            projectname=unicode(query2.value(PROJECTNAME).toString())
            taskid=query2.value(TASKID).toInt()[0]
            taskname=unicode(query2.value(TASKNAME).toString())
            duration=query2.value(DURATION).toFloat()[0]
            started_at=unicode(query2.value(STARTEDAT).toDateTime().toString(DATETIME_FORMAT))
            #started_at2=query2.value(STARTEDAT).toDateTime().date().toString('d').toInt()[0]  # Before we changed the SQL query to return just the day.
            started_at2=query2.value(STARTEDAT).toInt()[0]


            taskidsL.append(taskid)
            tasknameL.append(taskname)
            durationL.append(duration)
            started_at2L.append(started_at2)
            projectnameL.append(projectname)
               
            
        time_dict={'projectname':projectnameL,
                   'taskid':taskidsL,
                   'taskname':tasknameL,
                   'duration':durationL,
                   'date':started_at2L}
               
                
        #print time_dict
        
        data=pd.DataFrame(time_dict)
        
        #print data.head()
        
        table=data.pivot_table('duration',rows=['projectname','taskname'],cols='date',aggfunc=np.sum, fill_value=0)
            
        
        writer = pd.ExcelWriter('output.xlsx')
        table.to_excel(writer,'Sheet1')
        writer.save()            
            
        self.model.setQuery(query2)
        
        
    def initUI(self):
        
        #self.view = QtGui.QTableView()
        
        #self.tableView.setModel(self.model)
        
        self.setupUi(self) #method of table_view.py Ui_MainWindow
        
        self.tableView.setModel(self.model)
        
        mode = QtGui.QAbstractItemView.SingleSelection
        self.tableView.setSelectionMode(mode)
        
        self.connect(self.tableView, QtCore.SIGNAL('clicked(QModelIndex)'),self.onClicked)
        
        
        
        #self.setCentralWidget(self.view)
        
app = QtGui.QApplication([])
ex = Yahoo()
ex.show()
app.exec_()
        