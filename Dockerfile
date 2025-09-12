FROM python:3.10-slim

# Install system dependencies needed by WeasyPrint
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev \
#     python3-pip \
#     python3-setuptools \
#     python3-wheel \
#     python3-cffi \
#     libcairo2 \
#     libpango-1.0-0 \
#     libpangocairo-1.0-0 \
#     # libgdk-pixbuf2.0-0 \
#     libgdk-pixbuf-xlib-2.0-0 \
#     libffi-dev \
#     shared-mime-info \
#  && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Create the static output directory
# RUN mkdir -p dotscholar/assets/static/dist/
# RUN mkdir -p dotscholar/assets/media/

# (Optional) collect static if needed
# RUN python manage.py collectstatic --noinput || true
# Do not collect static as the required static assets are not uploaded to git

# Expose port 8000
EXPOSE 8000

# Start the Django app using gunicorn
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
