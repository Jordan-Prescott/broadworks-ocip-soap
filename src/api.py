import logging
import hashlib

import attr
import requests
from zeep import Client, Settings
from zeep.transports import Transport
from broadworks_ocip import BroadworksAPI
import broadworks_ocip.types

VERBOSE_DEBUG = 9


@attr.s(slots=True, kw_only=True)
class BroadworksSOAP:
    """TODO

    Attributes:


    Raises:
        e: [description]
        e: [description]

    Returns:
        [type]: [description]
    """

    wsdl_url: str = attr.ib()
    username: str = attr.ib()
    password: str = attr.ib()
    user_agent: str = attr.ib(default="BroadworksSOAP (TODO: Add link to docs)")

    ocip = attr.ib(default=None)

    soap_client: Client = attr.ib(default=None)
    session_id: str = attr.ib(default=None)
    timeout: int = attr.ib(default=10)

    logger: logging.Logger = attr.ib(default=None)
    authenticated: bool = attr.ib(default=False)

    def __attrs_post_init__(self) -> None:
        """AI is creating summary for __attrs_post_init__"""

        # wrap around this object
        self.ocip = BroadworksAPI(
            host="REQUIRED ARGUMENT",
            username=self.username,
            password=self.password,
            logger=self.logger if self.logger else None,
        )

        self.session_id = self.ocip.session_id
        self.logger = self.ocip.logger
        self.authenticated = False

        self.setup_soap_client()
        self.authenticate()

    def setup_soap_client(self) -> None:
        """
        Set up the SOAP client using requests and zeep.
        """
        session = requests.Session()
        session.auth = (self.username, self.password)
        session.verify = True
        session.headers.update({"User-Agent": self.user_agent})
        transport = Transport(session=session, timeout=self.timeout)
        settings = Settings(strict=False, xml_huge_tree=True)
        try:
            self.soap_client = Client(
                wsdl=self.wsdl_url + "?wsdl", transport=transport, settings=settings
            )
            self.logger.info("SOAP client initialised successfully.")
        except Exception as e:
            self.logger.error("Failed to initialize SOAP client.", exc_info=True)
            raise e

    def command(self, command, **kwargs) -> broadworks_ocip.base.OCICommand:
        """
        Send a command to the server via SOAP and decode the response.
        ### SOAP CHANGE: This method now uses the SOAP client instead of a socket.
        """
        # Instead of managing a persistent socket connection and authentication,
        # we assume that the SOAP client is already set up.
        xml = self.ocip.get_command_xml(command, **kwargs)
        self.logger.info(f">>> {command}")
        self.logger.log(VERBOSE_DEBUG, f"SEND: {str(xml)}")
        try:
            # Call the SOAP method (assumed to be processOCIMessage) with the XML.
            # Zeep typically expects a string, so we decode the bytes.
            soap_response = self.soap_client.service.processOCIMessage(xml)
            self.logger.log(VERBOSE_DEBUG, f"SOAP RESPONSE: {str(soap_response)}")
        except Exception as e:
            self.logger.error("SOAP service call failed", exc_info=True)
            raise e

        # Ensure the response is in bytes for decoding
        if isinstance(soap_response, str):
            response_bytes = soap_response.encode("ISO-8859-1")
        else:
            response_bytes = soap_response

        return self.ocip.decode_xml(response_bytes)

    def authenticate(self) -> broadworks_ocip.base.OCICommand:
        """
        Authenticate the connection to the OCI-P server.
        """

        auth_resp = self.command("AuthenticationRequest", user_id=self.username)
        authhash = hashlib.sha1(self.password.encode()).hexdigest().lower()
        signed_password = (
            hashlib.md5(":".join([auth_resp.nonce, authhash]).encode())
            .hexdigest()
            .lower()
        )
        login_resp = self.command(
            "LoginRequest14sp4", user_id=self.username, signed_password=signed_password
        )
        self.authenticated = True
        return login_resp
