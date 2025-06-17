# Call-Log-Handler

### TASK:

Design, implement, and demonstrate a simple "demo" application developed using the Python programming language that performs the following functionalities:

- Accept as input/configuration the path to a folder in the filesystem containing files in CSV format, which represent call log data.
- Identify the files, open them, and extract the call log data.
- Structure the data into JSON dictionaries.
- Persist this data in an external datastore.

> It is **not necessary** to implement the external datastore itself, as it will be managed by a library developed by a third party (external company). 
> The external company may implement the datastore using various heterogeneous technologies, e.g., a simple file on the filesystem or a NoSQL database (e.g., MongoDB), etc. 
> When designing the solution, consider that different installations might require different technologies (e.g., file-based in one case, NoSQL DB in another).

Therefore, evaluate:

- What kind of abstraction should be implemented for the library to support a potentially evolving path where different implementations using different technologies for the external datastore will be developed and used.
- What requirements/specifications should be requested/provided to the external company that will develop the persistent datastore management libraries.

### DETAIL

- **Objective:**
      - Develop an application that:
          - Reads CSV files from a directory.
          - Converts the data into JSON-like dictionaries.
          - Saves them into a datastore using an external library provided by third parties,
            which exposes a persistence management service.

- **Design Requirements:**
      - Clearly separate:
          - CSV file parsing.
          - Call modeling (CallLog as an OOP entity).
          - Datastore access interface.

### CONSTRAINTS

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

### RATIONALE OF THE EXERCISE

- Experiment with object-oriented design techniques.
- Experiment with setting up a development environment and defining the software structure.
- Experiment with simple techniques for data acquisition and parsing.
- Experiment with simple techniques for data modeling and transformation into JSON-serializable dictionaries.
- Experiment with defining interactions with components developed by third parties.

### ACCESSORY DATA

<details>
    <summary>Example of CSV content:</summary> 
    timestamp,caller,receiver,duration,status,uniqueCallReference<br>
    2025-05-14T10:23:00,1234567890,0123456789,120,successfully_completed,AABBCCDD<br> 
    2025-05-14T10:24:00,2345678901,3456789012,0,called_busy,EEFFGGHH
</details>

### INITIAL SUGGESTIONS

Try to identify the 4 main entities that make up the application and apply the principle of **"separation of concerns"** by abstracting these 4 main entities using an object-oriented design.

### Extra modules

- Create a module to randomly generate a collection of logs for testing the program.
- Refactor the code to adopt a generator-based approach using the yield statement.
- Create the dataStore module to insert the logs into an Elasticsearch node running in Docker.
- add logging
- refactor datastore to allow insertion to both elasticsearch and filesystem
