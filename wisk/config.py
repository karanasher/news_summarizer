# It is a neat practice to keep configs in a separate file.

class Config:
    # Ideally, you want these to be environment variables. But because we did not want to
    # ssh into the ec2 instance created by AWS Elastic Beanstalk, we are keeping this as it is.
    SECRET_KEY = 'a2b564d2271fff06c772fa5081a1b8e2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # This will create a db in the current main directory.
