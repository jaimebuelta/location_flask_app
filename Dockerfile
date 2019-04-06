# This stage installs and compiles the dependencies
# it requires compilers. After that, the compiled
# code is used in the runtime-image
FROM alpine:3.9 AS compile-image

# Add requirements for python and pip
RUN apk add --update python3 pytest

RUN mkdir -p /opt/code
WORKDIR /opt/code

# Get and install python dependencies
ARG BUILD_DEPS="python3-dev build-base gcc linux-headers postgresql-dev"
RUN apk add $BUILD_DEPS

# Install the requirements in user, so they are installed in /root/.local
ADD requirements_server.txt /opt/code
RUN pip3 install --user -r requirements_server.txt
ADD requirements.txt /opt/code
RUN pip3 install --user -r requirements.txt


# This stage is a small version that will be run
FROM alpine:3.9 AS runtime-image

# Install the runtime dependencies
RUN apk add --update python3 postgresql-libs curl pytest

# Add uwsgi configuration
RUN mkdir -p /opt/server
ADD ./docker/server/uwsgi.ini /opt/server

# Carry over the compiled dependencies
COPY --from=compile-image /root/.local /root/.local
# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

ADD ./docker/server/start_server.sh /opt/server

# Add code
ADD ./src/ /opt/code/

WORKDIR /opt/code

EXPOSE 80
CMD ["/bin/sh", "/opt/server/start_server.sh"]
HEALTHCHECK CMD curl --fail http://localhost/healthcheck/
