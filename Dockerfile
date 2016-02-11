############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:14.04

# Set the file maintainer (your name - the file's author)
MAINTAINER Alisson Aguiar Müller

# Update the default application repository sources list
# and install system dependencies
RUN apt-get update \
&& apt-get install -y software-properties-common \
&& add-apt-repository ppa:webupd8team/java \
&& apt-get update \
&& echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
&& apt-get install -y \
    oracle-java8-installer \
    python \
    python-pip \
    apache2 \
    libapache2-mod-wsgi \
    phantomjs \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY dependencies /dependencies
RUN pip install -r /dependencies/requirements.txt

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=recomendacao
# Local directory with project package
ENV DOCKYARD_PKG=recomendacao
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=${DOCKYARD_SRVHOME}/${DOCKYARD_SRC}
# Run in non-interactive mode
ENV DEBIAN_FRONTEND noninteractive
# Django settings for this container
ENV DJANGO_SETTINGS_MODULE=${DOCKYARD_PKG}.settings_local

# Create application subdirectories
WORKDIR ${DOCKYARD_SRVHOME}
RUN mkdir media static logs
VOLUME ["${DOCKYARD_SRVHOME}/media/", "${DOCKYARD_SRVHOME}/logs/"]

# Copy application source code to SRCDIR
COPY ${DOCKYARD_SRC} ${DOCKYARD_SRVPROJ}

# Copy local templates directory to container
COPY templates /templates

# Port to expose
EXPOSE 80

# Copy entrypoint script into the image
WORKDIR ${DOCKYARD_SRVPROJ}
COPY ./docker-entrypoint.sh /
