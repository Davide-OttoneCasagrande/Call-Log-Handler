# Call-Log-Handler

## Design Requirement Specification Document


<div align='right'> <b> Authors </b> <br> davide Ottone Casagrande</div>

### REVISION HISTORY

Version | Data | Author(s)| Notes
---------|------|--------|------
0 | 25/05/20 | Davide Ottone Casagrande | First Versionn of the document. Document Template
0.1 | 25/05/20 | Davide Ottone Casagrande | added introduction, and project constraints
1 | 25/05/21 | Davide Ottone Casagrande | added Class diagramm & description
1.1 | 25/05/26 | Davide Ottone Casagrande | modified and approved Class diagramm & description
1.2 | 25/05/26 | Davide Ottone Casagrande | added sequence diagram (dynamic model)
## Table of Content

1. [Introduction](#intro)
    1. [Technologies used](#tech)
    2. [Assumptions and Constraints](#constraints)
2. [System Overview](#system-overview)
    1. [System Architecture](#architecture)
    2. [System Interfaces](#interfaces)
    3. [System Data](#data)
        1. [System Inputs](#inputs)
        2. [System Outputs](#outputs)
3. [Structure](#struct)
    1. [Structural Diagrams](#sd)
        1. [Class Diagram](#cd)
            1. [Class Description](#cd-description)
2. [Object Diagram](#od)
3. [Dynamic Models](#dm)

##  <a name="intro"></a>  1 Introduction
Design, implement, and demonstrate a simple "demo" application developed using the Python programming language that performs the following functionalities:

- Accept as input/configuration the path to a folder in the filesystem containing files in CSV format, which represent call log data.
- Identify the files, open them, and extract the call log data.
- Structure the data into JSON dictionaries.
- Persist this data in an external datastore.

>- It is **not necessary** to implement the external datastore itself, as it will be managed by a library developed by a third party (external company).  
>- The external company may implement the datastore using various heterogeneous technologies, e.g., a simple file on the filesystem or a NoSQL database (e.g., MongoDB), etc.  
>- When designing the solution, consider that different installations might require different technologies (e.g., file-based in one case, NoSQL DB in another).

Therefore, evaluate:
- What kind of abstraction should be implemented for the library to support a potentially evolving path where different implementations using different technologies for the external datastore will be developed and used.
- What requirements/specifications should be requested/provided to the external company that will develop the persistent datastore management libraries.


### <a name="tech"></a> 1.1 Technologies used
- Pyhton

### <a name="constraints"></a> 1.2 Assumption and Constraint 
- Carry out a **design phase** before developing the application. You are free to choose the method of describing the design, which will be reviewed with the tutors before starting development activities.
- Use an **object-oriented design approach**; in particular, aim for a **modular design** based on the **"separation of concerns"** paradigm.
- A simple design could be based on:
    - A table defining each class that makes up the application, along with a textual description of the responsibilities of each class.
    - A description, even textual, of the **macro-interactions** expected between the classes.
- Try to structure the source code in a way that is consistent with the modularity of the design.
- The use of ChatGPT is allowed **only** for:
    - Specific support related to language syntax.
    - Use of Python libraries for reading CSV files and handling JSON dictionaries.
    - Learning about general OO topics (e.g., modularity/separation of concerns).
    - Using a Python development environment (IDE).
- **ChatGPT is NOT allowed** for defining the **overall structure** of the application.   

## <a name="system-overview"></a>  2 System Overview

### <a name="architecture"></a>  2.1 System Architecture

### <a name="interfaces"></a>  2.2 System Interfaces

### <a name="data"></a>  2.3 System Data
- Call Logs in .csv obtained from the file system
- expose a list of json obj with  an interface

#### <a name="inputs"></a>  2.3.1 System Inputs
The folder path string of the log.csv files can be provided either as a main argument or defined as a configurable constant.

#### <a name="outputs"></a>  2.3.2 System Ouputs
a list of json callLog class objects exposed by an interface

## <a name="struct"></a>  3 Structure

### <a name="sd"></a>  3.1 Structural Diagrams

#### <a name="cd"></a>  3.1.1 Class diagram
::: mermaid
classDiagram
    Loader ..> LogCollector
    LogCollector *-- CallLog
    LogCollector -- IToDataStore

    class Loader {
        +CSVLoader(filePath) list
    }

    class LogCollector {
        list CallLogs 
        +__init__()
    }

    class CallLog {
        datetime timestamp
        str caller
        str receiver
        int duration
        str status
        str UniqueCallReference
        +__init__(str)
        +__json__() json
    }

    class IToDataStore
    <<interface>> IToDataStore
    IToDataStore : insert(CallLog)
    
:::
##### <a name="cd-description"></a>  3.1.1.1 Class Description
- Loader
    - load the logs from an external source  filePath
- CallLog
    - instaciable class
    - each intance rapresent one log
- LogCollectionToJson
    - build a list of CallLogs
- IToDataStore
    - interface that expose the list for third party software

#### <a name="od"></a>  3.1.2 Object diagram

#### <a name="dm"></a>  3.2 Dynamic Models
::: mermaid
sequenceDiagram
LogCollector->>+Loader: load from CSV file
Loader-->>-LogCollector: string list
create participant CallLog
LogCollector->>+CallLog: Instance
LogCollector->>CallLog: call __json__()
CallLog-->>-LogCollector: answer
LogCollector->>+IToDataStore:insert
:::