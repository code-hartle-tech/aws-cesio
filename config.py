import os
import configparser

AWS_CONFIG_FILE = os.path.expanduser("~/.aws/config")
AWS_CREDENTIALS_FILE = os.path.expanduser("~/.aws/credentials")

def get_aws_profiles():
    """Retrieve all AWS profiles from ~/.aws/config and ~/.aws/credentials"""
    profiles = set()

    if os.path.exists(AWS_CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(AWS_CONFIG_FILE)
        
        for section in config.sections():
            if section.startswith("profile "):
                profiles.add(section.replace("profile ", ""))
            else:
                profiles.add(section)

    if os.path.exists(AWS_CREDENTIALS_FILE):
        credentials = configparser.ConfigParser()
        credentials.read(AWS_CREDENTIALS_FILE)
        profiles.update(credentials.sections())

    return sorted(profiles)

def get_aws_region(profile):
    """Retrieve the AWS region for the selected profile from ~/.aws/config"""
    default_region = "us-east-1"  # Fallback region if none is found

    if os.path.exists(AWS_CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(AWS_CONFIG_FILE)

        profile_section = f"profile {profile}" if profile != "default" else "default"

        if config.has_section(profile_section) and config.has_option(profile_section, "region"):
            return config.get(profile_section, "region")
        
        if config.has_section(profile) and config.has_option(profile, "region"):
            return config.get(profile, "region")

    return default_region  # Ensure we always return a valid region

AWS_PROFILE = None
AWS_REGION = None
