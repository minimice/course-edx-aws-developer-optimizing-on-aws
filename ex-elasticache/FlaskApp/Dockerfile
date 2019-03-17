FROM amazonlinux:2017.09

# install python requirements
RUN yum install -y python36 httpd24.x86_64 mod24_wsgi-python36

# Optional challenge
### Build from ~/environment/ex-elasticache/FlaskApp
# docker build -t ex-elasticache:latest .

### Running
# docker run --name ex-elasticache -it \
# -v /home/ec2-user/.aws:/root/.aws \
# -e MEMCACHED_HOST=pricing-cache.qaxlxp.0001.usw2.cache.amazonaws.com:11211 \
# -p 8080:8080 \
# ex-elasticache:latest

COPY . .

# Add and install Python modules
RUN pip-3.6 install -r ./requirements.txt

EXPOSE 8080

CMD ["python36", "application.py"]
