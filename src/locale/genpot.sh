# Generate the template file.

# Settings
PROJECT_ID_VERSION="woeusb"
REPORT_MSGID_BUGS_TO="https://github.com/slacka/WoeUSB/issues"

xgettext -C -k_ --package-name=$PROJECT_ID_VERSION --msgid-bugs-address=$REPORT_MSGID_BUGS_TO \
  -o woeusb.pot --foreign-user --from-code=UTF-8 \
  $(find .. -name '*.cpp' -or -name "*.hpp" -or -name "*.c" -or -name "*.h")
