FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

COPY main.py request_service.py ./

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "CICD_pt2", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
