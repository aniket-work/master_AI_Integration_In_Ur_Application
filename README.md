# master_AI_Integration_In_Ur_Application
master_AI_Integration_In_Ur_Application


**Prerequisites:**

* Python installed on your system.
* A basic understanding of virtual environments and command-line tools.

**Steps:**

1. **Virtual Environment Setup:**

   - Create a dedicated virtual environment for our project:
   
     ```bash
     python -m venv master_AI_Integration_In_Ur_Application 
     ```

   - Activate the environment:
   
     * Windows:
        ```bash
        master_AI_Integration_In_Ur_Application\Scripts\activate
        ```
     * Unix/macOS:
        ```bash
        source master_AI_Integration_In_Ur_Application/bin/activate
        ```

2. **Install Project Dependencies:**

   - Grab the necessary packages with the help of `pip`:
   
     ```bash
     pip install -r requirements.txt
     ```
     
3. **Run Server**

  ```bash
    python server.py
    
    #test
    curl -s http://127.0.0.1:5000/supply-chain-data?query=order_tracking
    
    #start mapping server
    python mapping_api.py
    
    
  ```
4. 


   


