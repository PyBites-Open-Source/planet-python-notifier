# Pybites new article email notifications

This is a quick script to use Sendgrid to send email notifications for new Pybites articles.

- It reads the feed on codechalleng.es' API.
- It loads in Sendgrid and from/to emails from the environment.
- It can look N days back.
- It uses a GitHub action to run the script every morning upon manual triggering.
