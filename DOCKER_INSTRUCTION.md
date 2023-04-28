# How to run this Dockerfile locally

## As of now Dockerfile is configured to use gunicorn in order to deploy our app in Render.com
## This is specified in CMD block of Dockerfile.
## In order to use Dockerfile locally please enter following command:

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"
```

`sh -c "flask run --host 0.0.0.0"` part overwrites what is in CMD block in Dockerfile