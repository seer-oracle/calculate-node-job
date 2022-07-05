FROM 420811272222.dkr.ecr.ap-southeast-1.amazonaws.com/rinz-staging-ecr:pythonbase_v3

# Todo check local timezone or remove?
RUN apk add --no-cache tzdata git && cp /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
    && echo "Asia/Ho_Chi_Minh" > /etc/timezone && export PYTHONPATH="${PYTHONPATH}:/webapps/rinz-io"

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libffi-dev libva-intel-driver supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && rm -rf /tmp/* /var/cache/*

COPY requirements.txt /
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.txt && mkdir -p /var/log/apps

COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps/rinz-io

WORKDIR /webapps/rinz-io
