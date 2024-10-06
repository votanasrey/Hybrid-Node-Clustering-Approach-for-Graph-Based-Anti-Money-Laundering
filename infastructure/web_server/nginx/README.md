### Generating SSL Certificates

For secure communication, it's essential to use SSL certificates. This project uses OpenSSL to generate a self-signed SSL certificate. Follow the steps below to create your certificate and key:

1. **Open your terminal**: Start by opening your terminal application.

2. **Navigate to your project directory**: Use the `cd` command to navigate to the root directory of your project.

    ```bash
    cd /nginx
    ```

3. **Create the SSL directory**: If it doesn't already exist, create a directory to store your SSL certificate and key. This guide assumes you're storing them in `ssl` within your project directory.

    ```bash
    mkdir -p ssl
    ```

4. **Generate the SSL certificate and key**: Run the following OpenSSL command. This command generates a new SSL certificate (`nginx.crt`) and private key (`nginx.key`), storing them in the previously created `ssl` directory. The certificate will be valid for 365 days.

    ```bash
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/nginx.key -out ssl/nginx.crt
    ```

    You will be prompted to enter details for your certificate (e.g., country, state, organization). These can be left blank for a self-signed certificate.

5. **Reference the certificate in your application**: Ensure your application or web server configuration references the newly created certificate and key. For example, in an Nginx configuration, you would specify the paths to `nginx.crt` and `nginx.key`.

After completing these steps, your application should be configured to use HTTPS for secure communication.