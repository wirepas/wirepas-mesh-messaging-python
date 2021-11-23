FROM python:3.8.8-alpine3.12 AS builder

RUN adduser --disabled-password wirepas

# Install required package to build protobuf lib
RUN apk add --no-cache gcc bash build-base git protobuf make musl-dev python3-dev
RUN ln -sf /usr/lib/libprotobuf.so.23 /usr/lib/libprotobuf.so

RUN python3 -m pip install wheel setuptools pkgconfig

USER wirepas
WORKDIR /home/wirepas

# Protobuf checkout
RUN git clone https://github.com/protocolbuffers/protobuf.git
RUN cd protobuf && git checkout v3.12.2
WORKDIR /home/wirepas/protobuf/python

RUN export LD_LIBRARY_PATH=/usr/lib/

# Build and Install Packages as user to be copied in runner
RUN CFLAGS="-g0" python3 setup.py clean build install --cpp_implementation --user

# Six in needed by protobuf
RUN pip3 install six --user

# Build and Install Wirepas messaging
RUN mkdir /home/wirepas/wmm
WORKDIR /home/wirepas/wmm

# It works only with our Github action
COPY ./artifact/wirepas_mesh_messaging*.whl .
RUN pip3 install *.whl --user

# Build the final image
FROM python:3.8.8-alpine3.12 as tester

RUN adduser --disabled-password wirepas

RUN apk add --no-cache libprotobuf

RUN pip3 install pytest
# Run the test to validate the image
RUN mkdir tests
COPY --chown=wirepas ./tests ./tests

USER wirepas

ENV PATH="/home/wirepas/.local/bin:${PATH}"

# Copy the built wheel and its dependencies from builder
COPY --from=builder /home/wirepas/.local /home/wirepas/.local

RUN pytest -p no:cacheprovider ./tests

# Build the final image
FROM python:3.8.8-alpine3.12 as runner

# Variable set from CI
ARG WIREPAS_MESH_MESSAGING_BUIL_SHA1=unset

RUN adduser --disabled-password wirepas

RUN apk add --no-cache libprotobuf

USER wirepas

ENV PATH="/home/wirepas/.local/bin:${PATH}"

# Copy the built wheel and its dependencies from builder
COPY --from=builder /home/wirepas/.local /home/wirepas/.local

LABEL com.wirepas.wmm.build.sha1="${WIREPAS_MESH_MESSAGING_BUIL_SHA1}"
