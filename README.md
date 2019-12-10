# Azure Functions (Python)
Samples / Templates of Azure Function Apps with Python

## Local Setup (Debugging)

### Command Line
Run the function apps from your command line locally.
1. Make sure [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2) is installed.  
2. Make sure `python 3.6+` and required libraries are installed.     
3. Make sure you are on the `azure` branch. Use command `func host start` to run the function app locally.   

### VS Code
VS Code IDE provides more control fpr local deployment while providing debugging, repo control, and also deployment to azure portal as integrated features.

1. Install Azure Extensions:
 - Azure Account 
 - Azure CLI Tools
 - Azure Functions
 - Azure Repos
 - Python
 
 
2. Open GM Folder
3. Open Command Pallette (`Ctrl+Shift+P` or `F1`), and select  `Azure Functions: Initialize Project for use with VS Code` and follow prompts

4. Open Command Pallette (`Ctrl+Shift+P` or `F1`), and select  `Python: Select Interpreter` and select eithe conda environments or relative venv created.

Sample of `.vscode\settings.json` setting if local folder `.venv` is selected and set as python interpreter:
```json
		# .vscode\settings.json
	{
	  "azureFunctions.pythonVenv": ".venv",
	  "python.pythonPath": ".venv\\Scripts\\python.exe",
	  "azureFunctions.deploySubpath": "AzureFunction.zip",
	  "azureFunctions.scmDoBuildDuringDeployment": true,
	  "azureFunctions.projectLanguage": "Python",
	  "azureFunctions.projectRuntime": "~2",
	  "azureFunctions.preDeployTask": "func: pack --build-native-deps",
	  "debug.internalConsoleOptions": "neverOpen",
	}
```


Sample of `.vscode\settings.json` using conda environment as python interpreter. This assumes a windows environment variable `CONDAPATH` is defined pointing to conda installation path.  It can be replaced with absolute path of conda which in default case is as follow  `CONDAPATH = 'C:\Users\<YOUR USERNAME>\AppData\Local\Continuum\miniconda3\'`.

This might require a single time running of `conda init powershell` command in terminal window of VS Code.

```json
		# .vscode\settings.json
	{
	  "azureFunctions.pythonVenv": "%CONDAPATH%\\envs\\azure",
	  "python.pythonPath": "%CONDAPATH%\\azure\\Scripts\\python.exe",
	  "azureFunctions.deploySubpath": "AzureFunction.zip",
	  "azureFunctions.scmDoBuildDuringDeployment": true,
	  "azureFunctions.projectLanguage": "Python",
	  "azureFunctions.projectRuntime": "~2",
	  "azureFunctions.preDeployTask": "func: pack --build-native-deps",
	  "debug.internalConsoleOptions": "neverOpen",
	}
```


## Shared Code
The first three example listed below demonstrate various arrangements of shared/common code in Azure python functions.
 - FuncApp-Http-Py-OptionA
 - FuncApp-Http-Py-OptionB
 - FuncApp-Http-Py-OptionC


## Database Connection
The other example provides the basis for handling Azure SQL servers and databases.
 - FuncApp-Http-sql-Example

Note the deployment details mentioned in following sections.

### Local Settings with DB (VS Code)
For local code development and debugging, you can define an application setting variable, e.g.  `'dbConnectionValue'`, under `'Values'` element of `'local.settings.json'`. Note that in example shown below, the variable `'dbConnectionValue'` is visible in python code during local deployment and debugging.
```json
  # local.settings.json

  {
    "IsEncrypted": false,
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "Values": {
      "FUNCTIONS_WORKER_RUNTIME": "python",
      "dbConnectionValue": "Driver={ODBC Driver 13 for SQL Server};Server=tcp:<your db server>.database.windows.net,1433;Database=<your db>;Uid=<your user>@<your db>;Pwd=<your pass>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    },
    "ConnectionStrings": {
      "sqlConnectionString": "Driver={ODBC Driver 17 for SQL Server};Server=tcp:<your db server>.database.windows.net,1433;Database=<your db>;Uid=<your user>@<your db>;Pwd=<your pass>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    }
  }
```
Since `'SQLAZURECONNSTR_sqlConnectionString'` is not available in local deployment environment, we
After the configuration is completed, to have a smooth database access  string variable for database is available to python scripts and can be accessed as  + **name of connection string** (e.g. *'sqlConnectionString'* in the above setup):

   ```Python
     # Azure Function:  Python Code
     # Database Connection String access to support both Portal and Local deployment
     try:
         # Azure Portal Deployment
         connStr = "SQLAZURECONNSTR_sqlConnectionString"
         db = pyodbc.connect( os.environ.get(connStr) )

     except Exception as e1:
         try:
             # Local Deployment
             connStr = "dbConnectionValue"
             db = pyodbc.connect( os.environ.get(connStr) )

        except Exception as e2:
               return "%s \n %s" %(str(e1),str(e2)), os.environ.get(connStr)             

     cursor = db.cursor()
     cursor.execute("SELECT * FROM table1")    
   ```

#### Local Deployment/Debugging Settings with DB (VS Code)
For deployment of code developed locally, if you have database connection (e.g. using pyodbc), you want to build dependencies locally to avoid `pyodbc` module not found error when deployed and triggered via azure portal. 

Once the azure function project is initialized for use in VS code, the  `azureFunctions.preDeployTask` parameter in  `.vscode\settings.json` can be modified as 
```json
  # .vscode\settings.json
	"azureFunctions.preDeployTask": "func: pack --build-native-deps"
```

Note that this feature will require a docker daemon (e.g. docker desktop for windows) to be running. The docker needs to be running with linux containers.


### Azure Portal Deployment Settings with DB
  **Warning**: Use `ODBC Driver 17` ONLY (<s>`ODBC Driver 13`</s> is **NOT** working currently as of October 2010)

  Standard process to set connection string for Azure functions is as below.
   - Navigate to Function Apps on Azure portal
   - Select your Function App named *'Function Name'*
   - Select *'Platform features'* tab
   - Select *'Configuration'* item
   - Press *'New connection string'* Under *'Connection strings'* section
   - Set the string on *'Add/Edit connection string'* dialogue opened

 > **Name:** "sqlConnectionString"
 >
 > **Value:** "Driver={ODBC Driver 17 for SQL Server};Server=tcp:\<your db server\>.database.windows.net,1433;Database=\<your db\>;Uid=\<your user\>@\<your db\>;Pwd=\<your pass\>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
 >
 > **Type:** 'SQLAzure'

 **Warning:** The connection string can be obtained from your Azure SQL with ODBC; However, be sure to use `ODBC Driver 17` as <s>`ODBC Driver 13`</s> is *NOT* working on azure portal.
   - Press *'OK'* on 'Add/Edit connection string' dialogue opened
   - Press *'Save'* button on top of Configuration

After the configuration is completed, the connection string variable for database is available to python scripts and can be accessed as `'SQLAZURECONNSTR_'` + **name of connection string** (e.g. *'sqlConnectionString'* in the above setup):
   ```Python
     # Azure Function:  Python Code
     # Database Connection String can be accessed in python as below
     connStr = "SQLAZURECONNSTR_sqlConnectionString"
     db = pyodbc.connect( os.environ.get(connStr) )
     cursor = db.cursor()
     cursor.execute("SELECT * FROM table1")    
   ```
Alternatively as discuss below for local deployment, the connection string can  be defined as a variable under *'Application settings'* and used in python. The steps to add an application setting variable is quite similar to adding connection string except it is initiated with the following:
 - Press *'New application setting'* Under *'Application settings'* section

After the configuration is completed, the application setting variable for database is available to python scripts and can be accessed as **name of application setting variable** (e.g. *'sqlConnectionValue'*):
  ```Python
    # Azure Function:  Python Code
    # Database Connection String can be accessed in python as below
    connStr = "sqlConnectionValue"      # *** Your defined application setting variable ***
    db = pyodbc.connect( os.environ.get(connStr) )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM table1")    
  ```


