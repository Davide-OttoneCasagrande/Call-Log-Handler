# Call-Log-Handler

## Design Requirement Specification Document


<div align='right'> <b> Authors </b> <br> davide Ottone Casagrande</div>

### REVISION HISTORY

Version | Data | Author(s)| Notes
---------|------|--------|------
0.0 | 25/05/20 | Davide Ottone Casagrande | First Versionn of the document. Document Template
0.1 | 25/05/20 | Davide Ottone Casagrande | added introduction, and project constraints
1.0 | 25/05/21 | Davide Ottone Casagrande | added Class diagramm & description
1.1 | 25/05/26 | Davide Ottone Casagrande | modified and approved Class diagramm & description
1.2 | 25/05/26 | Davide Ottone Casagrande | added sequence diagram (dynamic model)
1.3 | 25/05/27 | Davide Ottone Casagrande | modified and approved sequence diagram (dynamic model)
2.0 | 25/05/27 | Davide Ottone Casagrande | updated structure drs.md and written new system modules
2.1 | 04/06/27 | Davide Ottone Casagrande | Separated generation logic into its own module and restructured project for stricter OOP design
2.2 | 04/06/27 | Davide Ottone Casagrande | refactored system module 1 around python generator (yield statemment)

## Table of Content

1. [Introduction](#intro)
    1. [Purpose and Scope](#purpose)  
    2. [Definitions](#def)
    3. [Bibliography](#biblio)
2. [Project Description](#description)
    1. [Technologies used](#tech)
    2. [Assumptions and Constraints](#constraints)
3. [System Overview](#system-overview)
    1. [System Architecture](#architecture)
    2. [System Interfaces](#interfaces)
    3. [System Data](#data)
        1. [System Inputs](#inputs)
        2. [System Outputs](#outputs)
4. [System Module 1:Logs collector](#sys-module-1)
    1. [Structural Diagrams](#sd)
        1. [Class Diagram](#cd)
            1. [Class Description](#cd-description)
        2. [Object Diagram](#od)
        3. [Dynamic Models](#dm)
5. [System Module 2: Random logs generator](#sys-module-2)
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
    
### <a name="purpose"></a> 1.1 Purpose and Scope
- Experiment with object-oriented design techniques.
- Experiment with setting up a development environment and defining the software structure.
- Experiment with simple techniques for data acquisition and parsing.
- Experiment with simple techniques for data modeling and transformation into JSON-serializable dictionaries.
- Experiment with defining interactions with components developed by third parties.

### <a name="def"></a> 1.2 Definitions
<details> 
    <summary> Define words, acronyms or sentence to clarify ambiguos meanings
    </summary>
    <p>within the boundary of this projects: </p>

    | terms         | definition    |
    | ------------- | ------------- |
    | Call log  | log of a TETRA call set up aptempt |
</details>

### <a name="biblio"></a> 1.3 Bibliography
<details> 
    <summary> external sources used in the making of this project:
    </summary>
    python library:<br>
    - os<br>
    - <br>
</details>

## <a name="description"></a> 2 Project Description
This project simulates the generation, processing, and storage of telecommunication call logs. It consists of a modular Python-based pipeline that:
- **Generates Random Call Logs**  
A log generator creates synthetic call records in CSV format, including fields like timestamp, caller/receiver IDs, duration, status, and a unique reference ID.
- **Parses and Converts Logs**  
A loader module reads the generated CSV file and converts each row into structured CallLog objects, which can be serialized to JSON.
- **Collects and Stores Logs**  
A collector module loads the logs and passes them to a data store interface. A temporary implementation of this interface writes the logs to a JSON file, with the path configurable via an .ini file.
- **Interface-Driven Design**  
The system uses an abstract interface (IToDataStore) to allow flexible integration with different storage backends (e.g., databases, APIs, cloud storage).
- **Configuration-Driven Paths**  
File paths for input and output are managed through a configuration file, enabling easy customization without modifying code.

### <a name="tech"></a> 2.1 Technologies used
- Python
- mermaid (for the graphic in the documentation)

### <a name="constraints"></a> 2.2 Assumption and Constraint 
<- Carry out a **design phase** before developing the application. You are free to choose the method of describing the design, which will be reviewed with the tutors before starting development activities.
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

## <a name="system-overview"></a>  3 System Overview
### <a name="architecture"></a>  3.1 System Architecture

   ::: mermaid

flowchart TD

    B0[logCSVGen]
    B1[randomLogs]

    A@{ shape: circle, label: "Start" } --> A0
    B@{ shape: circle, label: "Start" } --> B0
    B0 --> B1
    B1-->  Bs@{ shape: circle, label: "stop" } 

    A0[main]
    A1[loader]
    A3['temp'DataStore]

    A0 --> A1
    A1 --> A3 
    A3 --> As@{ shape: circle, label: "stop" } 
:::

### <a name="interfaces"></a>  3.2 System Interfaces

### <a name="data"></a>  3.3 System Data
- Call Logs in .csv obtained from the file system
- expose a list of json obj with  an interface

#### <a name="inputs"></a>  3.3.1 System Inputs
The folder path string of the log.csv files can be provided either as a main argument or defined as a configurable constant.

#### <a name="outputs"></a>  3.3.2 System Ouputs
a list of json callLog class objects exposed by an interface

## <a name="sys-module-1"></a>  4 System Module 1: Logs collector

### <a name="sd"></a>  4.1 Structural Diagrams

#### <a name="cd"></a>  4.1.1 Class diagram
::: mermaid
classDiagram

    IDataStore ..|> DataStore : implements
    CallLogLoader --> CallLog : loads
    Main --> CallLogLoader : uses
    Main --> DataStore : uses 


    class CallLog {
        -datetime timestamp
        -str caller
        -str receiver
        -int duration
        -str status
        -str uniqueCallReference
        +__init__(datetime, str, str, int, str, str)
        +to_json() str
    }
   
    class CallLogLoader {
        -Path folder_path
        +__init__(str)
        -__load_csv_files()
    }
    
    class IDataStore {
        <<interface>>
        +insert(list[str])
    }

    class DataStore { }

    
class Main {
        +main(int)
    }
:::

##### <a name="cd-description"></a>  4.1.1.1 Class Description
- CallLogLoader
    - load the logs from an external source  filePath
- CallLog
    - each intance rapresent one log
- IToDataStore
    - interface that expose the list for third party software

#### <a name="od"></a>  4.1.2 Object diagram


#### <a name="dm"></a>  4.2 Dynamic Models
::: mermaid
 sequenceDiagram
    actor User
    participant Main

    User->>+Main: Execute main()
    Main->>Main: Load configuration

    create participant CallLogLoader 
    Main->>CallLogLoader: Initialize with folder_path

    create participant DataStore
    Main->>DataStore: Initialize with export_file_path

    loop for each row for each file
    Main->>+CallLogLoader: Load CSV file
    create participant CallLog
    CallLogLoader->>CallLog: Create CallLog instances
    CallLogLoader-->>-Main: yield

    Main->>+DataStore: Insert logs to configured datastore
    DataStore--XCallLog: give me the json
    destroy CallLog
    CallLog->>DataStore: 
    Main-->>Main: Log progress when indicated
    end
    
    Main-->>-User: Log collection successfully exported

:::

## <a name="sys-module-1"></a>  5 System Module 2: Random logs generator

### <a name="sd"></a>  5.1 Structural Diagrams


#### <a name="cd"></a>  5.1.1 Class diagram
::: mermaid
classDiagram
    Logsfile *-- Call
    
class Call {
        -str timestamp
        -str caller
        -str receiver
        -int duration
        -str status
        -str uniqueCallReference
        +__str__() : str
    }

    class Logsfile {
        -list~str~ logs
        -int deltaT
        -int number_of_logs
        +__generate_random_timestamps(startingHour: datetime) : list[str]
    }
:::

#### <a name="cd-description"></a>  5.1.1.1 Class Description
- Call
    - generate a random log
- Logsfile
    - collect a list of random logs

#### <a name="od"></a>  5.1.2 Object diagram


#### <a name="dm"></a>  5.2 Dynamic Models
:::mermaid
 sequenceDiagram
    participant logCSVGen
    logCSVGen->>logCSVGen: loading config
    logCSVGen->>logCSVGen: random generation of number_of_files

    loop until iteration == number_of_files
    create participant Logsfile
    logCSVGen->>+Logsfile: random generation of a single Logsfile
    Logsfile->>+Logsfile: random generation of number_of_calls
    loop until iteration == number_of_calls
    create participant Call
    Logsfile->>+Call: random generation of a single Call
    Call->>Call: random generation of the attributes
    Call-->>-Logsfile:adding log to the collection
    end

    Logsfile-->>-logCSVGen:returning list[Call]
    logCSVGen->>FileSystem: saving Logsfile as .CSV
    end
:::