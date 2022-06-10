from django.shortcuts import render
import pandas as pd
import json
import os
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
import io
import sys



# Create your views here.
def home(request):
    return render(request, 'index.html')

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST['message']

        # send email
        send_mail(
            "Message from " + name,
            message,
            email,
            ['flashscriptspython@gmail.com'],
            )

        return_message = "Thank you, your message has been sent! "
        return render(request, 'index.html',{'return_message':return_message})
    else:
        return render(request, 'index.html')

def upload(request):
    return render(request, 'upload.html', {'name':"there"})

def load(request):
    #print(request.method)
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    return render(request, 'table.html')

def table(request):

    #print(request.method)
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)

    #print(request.FILES['document'].name)
    if request.FILES['document'].name[-3:-1] == 'cs':
        df = pd.read_csv(os.path.join(os.getcwd(),"media", request.FILES['document'].name))
    elif request.FILES['document'].name[-3:-1] == 'ls':
        df = pd.read_excel(os.path.join(os.getcwd(),"media", request.FILES['document'].name))

    # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    code = "#Code Starts Here: \n"
    code = code + "import pandas as pd \n"
    code = code + "import numpy as np \n"
    code = code + "import os \n"
    code = code + "# Import data \n"
    code = code + "df = pd.read_csv(os.path.join(os.getcwd(),'files','{}')) \n".format(request.FILES['document'].name)
    context = {'d': data, 
                'headers': list(data[0].keys()),
                'code':code,
                'action':''}

    return render(request, 'table.html', context)

def evaluate(request):
    # get existing code
    code = request.POST["code"]
    data = request.POST["data"]
    action = request.POST['selected_action']
    data = pd.DataFrame(list(eval(data)))

    nan_n = data.isnull().sum().sum()

    evaluation_message = "This dataset contains {} rows and {} columns. \n".format(len(data),len(data.columns))
    evaluation_message = evaluation_message + "{}/{} cells are empty. \n".format(nan_n, len(data)*len(data.columns))

    headers = data.columns
    # parsing the DataFrame in json format.
    json_records = data.reset_index().to_json(orient ='records')
    json_records = data.to_json(orient ='records')
    data = json.loads(json_records)

    context = {'d': data, 
                'headers': headers,
                'code':code,
                'action':action,
                'evalutation_message':evaluation_message}

    return render(request, "table.html", context)

def displayparameters(request):
    code = request.POST["code"]
    # get selected action
    action = request.POST['selected_action']
    #get evaluation message
    evaluation_message = request.POST['evaluation_message']
    data = request.POST["data"]
    data = pd.DataFrame(list(eval(data)))

    headers = data.columns
    # parsing the DataFrame in json format.
    json_records = data.reset_index().to_json(orient ='records')
    json_records = data.to_json(orient ='records')
    data = json.loads(json_records)
    #print(list(data[0].keys()))
    context = {'d': data, 
                #'headers': list(data[0].keys()),
                'headers': headers,
                'code':code,
                'action':action,
                'evalutation_message':evaluation_message}

    return render(request, "table.html", context)

def code_generation(request):

    def execute_eqn(data, include, parameter, operation, num2):
        if include == "Include":
            equation =  "df = df[(df['{}']{}{})]".format(parameter, operation, num2)     
            if operation == "==":
                    print(parameter)
                    print(data.columns)
                    try: data = data[data[parameter] == num2]
                    except: print("not a valid dunction")
            elif operation == ">=":
                    try: data = data[data[parameter] >= num2]
                    except: print("not a valid dunction")    
            elif operation == ">":
                    try: data = data[data[parameter] > num2]
                    except: print("not a valid dunction") 
            elif operation == "<=":
                    try: data = data[data[parameter] <= num2]
                    except: print("not a valid dunction") 
            elif operation == "<":
                    try: data = data[data[parameter] < num2]
                    except: print("not a valid dunction")        
        elif include == "Exclude":
            equation =  "df = df[~(df['{}']{}{})]".format(parameter, operation, num2)
            if operation == "==":
                    print(parameter)
                    print(data.columns)
                    try: data = data[~(data[parameter] == num2)]
                    except: print("not a valid dunction")
            elif operation == ">=":
                    try: data = data[~(data[parameter] >= num2)]
                    except: print("not a valid dunction")    
            elif operation == ">":
                    try: data = data[~(data[parameter] > num2)]
                    except: print("not a valid dunction") 
            elif operation == "<=":
                    try: data = data[~(data[parameter] <= num2)]
                    except: print("not a valid dunction") 
            elif operation == "<":
                    try: data = data[~(data[parameter] < num2)]
                    except: print("not a valid dunction")        
        

        return data, equation
    # get existing code
    code = request.POST["code"]
    # get selected action
    action = request.POST['selected_action']
    #get evaluation message
    evaluation_message = request.POST['evaluation_message']
    data = request.POST["data"]
    data = pd.DataFrame(list(eval(data)))
    print(action)

    if action == "renamecolumns":
        try:
            # get new column name
            newcolname = request.POST["newcolname"]
            # get old column name 
            oldcolname = request.POST["parameter"]   
            #execute
            data.rename(columns = {oldcolname:newcolname}, inplace = True)
        except: print("Error, check inputs")
        else:
            # update code
            code = code + "# Rename column {} to {}: \n". format(oldcolname, newcolname)
            #code = code + "df = df[~(df['index'] == {})] \n".format(ind)
            code = code + "df.rename(columns = {{'{}':'{}'}}, inplace = True) \n".format(oldcolname, newcolname)

    if action == "droptoprows":
        try:
            # get index number to remove
            ind = int(request.POST["num1"])           
            #execute
            #data = data[~(data["index"] == ind)]
            data = data.iloc[ind:]
        except: print("input not a valid index number")
        else:
            # update code
            code = code + "# Remove the top {} row(s): \n". format(ind)
            #code = code + "df = df[~(df['index'] == {})] \n".format(ind)
            code = code + "df = df.iloc[{}:] \n".format(ind)
    
    if action == "dropcolumn":
        try:
            # get index number to remove
            columns = request.POST["columns"]   
            #execute
            data.drop(columns=[columns], inplace = True)
            print(columns)
        except: print("Error")
        else:
            # update code
            code = code + "# Drop column {} \n".format(columns)
            code = code + "df = df.drop(columns = ['{}'], inplace = True) \n".format(columns)

    if action == "customizedcode":
        try:
            # get index number to remove
            customizedcode = request.POST["customizedcode"]
            comment = request.POST["comment"]         
            # update code
            code = code + "# {}\n". format(comment)
            #code = code + "df = df[~(df['index'] == {})] \n".format(ind)
            code = code + "{}\n".format(customizedcode)
            #execute
            variables = {'data':data}
            print('check point')
        
            customizedcode = "df = data;" + customizedcode.replace("df","data")
            print('check point')
            try: 
                print('check point')
                exec(customizedcode,variables)
                print('check point')
            except: print("not a valid customized command")
            else: data = variables['df']

            
        except: print("input not valid")
    
    if action == "dropna":
        try:
            # get index number to remove
            parameter = request.POST["parameter"] 
            print(parameter)          
            # update code
            code = code + "# Remove row if {} is empty (not a number): \n". format(parameter)
            code = code + "df = df[~(df['{}'].isna())] \n".format(parameter)
            #execute
            #data = data[~(data["index"] == ind)]
            data = data[~data[parameter].isna()]
        except: print("input not a valid index number")
    
    if action == "sort":
        try:
            # get index number to remove
            parameter = request.POST["parameter"] 
            order = request.POST["order"]        
            # update code
            if order == 'Ascending':
                code = code + "# Sort {} in ascending order \n". format(parameter)
                code = code + "df.sort_values(by = ['{}'], ascending= True, inplace = True)\n".format(parameter)
                data.sort_values(by = parameter, ascending=True,inplace = True)
            elif order == 'Descending':
                code = code + "# Sort {} in descending order \n". format(parameter, order)
                code = code + "df.sort_values(by = ['{}'], ascending= False, inplace = True)\n".format(parameter)
                data.sort_values(by = parameter, ascending=False,inplace = True)
        except: print("Not a valid function")

    if action == "conditionalfilter":
        try:
            # get index number to remove
            include = request.POST["include"] 
            parameter = request.POST["parameter"] 
            operation = request.POST["operation"] 
            num2 = request.POST["num2"]
            try: num2 = float(num2)
            except: print("Input is a string")
            else: print("Input is a number")

            # update code
            code = code + "# {} row if {} is {} {}: \n". format(include, parameter, operation, num2)
            equation =  "df = df[(df['{}']{}{})]".format(parameter, operation, num2)
            print(equation.replace("df", "data"))
            try: data, equation = execute_eqn(data, include, parameter, operation, num2)
            except:print("Not a valid function.")
            else:
                string = "{}\n".format(equation)
                code = code + string

        except: print("input not a valid index number")

    headers = data.columns
    # parsing the DataFrame in json format.
    json_records = data.reset_index().to_json(orient ='records')
    json_records = data.to_json(orient ='records')
    data = json.loads(json_records)
    #print(list(data[0].keys()))
    context = {'d': data, 
                #'headers': list(data[0].keys()),
                'headers': headers,
                'code':code,
                'action':action,
                'evalutation_message':evaluation_message}

    return render(request, "table.html", context)

def removecolumns(request):
    # get existing code
    code = request.POST["code"]
    # get columns
    cols = request.POST["columns"]
    # get data
    data = request.POST["data"]
    data = pd.DataFrame(list(eval(data)))
    
    # update code
    #print(cols)    

    #execute

    # parsing the DataFrame in json format.
    json_records = data.reset_index().to_json(orient ='records')
    json_records = data.to_json(orient ='records')
    data = json.loads(json_records)
    #print(list(data[0].keys()))
    context = {'d': data, 
                'headers': list(data[0].keys()),
                'code':code}
    return render(request, "table.html", context)