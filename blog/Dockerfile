# pull official base image
FROM jekyll/jekyll:3.8

# set work directory
WORKDIR /usr/src/blog


# RUN apt-get update \
#     && apt-get install -y ruby-full build-essential zlib1g-dev rubygems gcc

# RUN gem install bundler jekyll

# copy entrypoint.sh
COPY ./entrypoint.sh .

RUN gem install -n /usr/local/bin jekyll

# copy project
COPY . .

RUN chmod 1777 -R /usr/src/blog

# run entrypoint.sh
RUN chmod +x /usr/src/blog/entrypoint.sh
ENTRYPOINT ["/usr/src/blog/entrypoint.sh"]
