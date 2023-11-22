from setuptools import setup, find_packages

setup(
    name='deepsquare_bot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot==20.6',  # Make sure to specify the correct versions
        'openai',
        'python-dotenv',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'deepsquare-bot = deepsquare_bot.bot:main',
        ],
    },
)
