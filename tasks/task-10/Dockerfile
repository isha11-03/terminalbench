FROM python:3.12-slim
WORKDIR /workspace
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /workspace/requirements.txt
RUN apt-get update \
	&& apt-get install -y --no-install-recommends iverilog \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt
COPY . /workspace
RUN chmod +x /workspace/run-tests.sh /workspace/solution.sh
CMD ["bash", "run-tests.sh"]
