###########
Webservices
###########

Webservices is a key part in the sdmxthon library as it allows the user to interact with the SDMX APIs
and download data and metadata from them.

They are based on the :obj:`SdmxWebServiceConnection <sdmxthon.webservices.webservices.SdmxWebServiceConnection>`
interface. It holds all methods we are about to use to query the API, using the :obj:`QueryBuilder for SDMX API v1 <sdmxthon.webservices.query_builder.SdmxWs1>`
or the :obj:`QueryBuilder for SDMX API v2 <sdmxthon.webservices.query_builder.SdmxWs2p0>`

We can also interact with Fusion Metadata Registry by validating the data (:py:meth:`~sdmxthon.model.dataset.Dataset.fmr_validation`)
and uploading structures using the API method (:py:meth:`~sdmxthon.api.api.upload_metadata_to_fmr`)
or the bundled method (:py:meth:`~sdmxthon.model.message.Message.upload_metadata_to_fmr`)
in the :obj:`Message <sdmxthon.model.message.Message>` class.

.. toctree::
    :maxdepth: 2

    webservices/webservice_connection
    webservices/query_builder
    webservices/fmr