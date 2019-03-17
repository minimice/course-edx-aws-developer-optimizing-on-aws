FROM amazonlinux:2017.09

# install python requirements
RUN yum install -y python36 httpd24.x86_64 mod24_wsgi-python36 && sed -i "s/Listen 80/Listen 8081/g" /etc/httpd/conf/httpd.conf

# Copy app source and config
COPY conf/ /etc/httpd/conf.d/
COPY . /src

# Add and install Python modules
RUN pip-3.6 install -r /src/requirements.txt

EXPOSE 8081

CMD ["apachectl", "-DFOREGROUND"]
