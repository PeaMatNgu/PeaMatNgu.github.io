FROM ruby:3.3-bookworm

WORKDIR /srv/jekyll

COPY Gemfile ./
RUN gem install bundler && bundle install

EXPOSE 4000 35729

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--port", "4000", "--livereload", "--livereload-port", "35729", "--force_polling"]

