FROM python:3.11-slim

WORKDIR /task

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy task files
COPY . .

# Ensure scripts are executable
RUN chmod +x run-tests.sh solution.sh

CMD ["/bin/bash"]
