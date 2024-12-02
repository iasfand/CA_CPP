# SkyPort: Social Media for Airports

## Overview

SkyPort is a Flask-based application designed to provide social media functionalities tailored for airports. This guide will help you set up and run the application.

## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Git**: [Download and install Git](https://git-scm.com/)
- **Python**: [Download and install Python](https://www.python.org/downloads/)
- **AWS CLI**: [Download and install AWS CLI](https://aws.amazon.com/cli/)

## Setup Instructions

1. **Clone the Repository**  
   Clone the repository from GitHub:
   ```bash
   git clone https://github.com/iasfand/CA_CPP
   cd CA_CPP
   ```

2. **Configure AWS**  
   Set up your AWS credentials in the `.aws` directory. Ensure that you have a valid `credentials` file in this directory with your AWS access and secret keys configured. For more details, refer to the [AWS CLI Configuration Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

3. **Set Environment Variables**  
   Rename the `.env.example` file to `.env`:
   ```bash
   mv .env.example .env
   ```
   Open the `.env` file and fill in the required variables for the application.

4. **Install Dependencies**  
   Install the necessary Python packages listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**  
   Start the Flask application by running:
   ```bash
   flask run
   ```
   or:
   ```bash
   python3 application.py
   ```

6. **Access the Application**  
   The application will run on port `5000`. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Additional Notes

- Ensure that your AWS credentials and environment variables are correctly set up for smooth functionality.
- For any issues or contributions, please create an issue or pull request in the [GitHub repository](https://github.com/iasfand/CA_CPP).