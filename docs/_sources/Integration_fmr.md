# Integration with Fusion Metadata Registry

SDMXThon does only provide an API to interact with SDMX data and metadata with Python, using SDMX-ML as an interface, but it does not provide any repository to store metadata and data, or any graphical interface or tool to manage information. Therefore, use of SDMXThon within statistical organisations must be seen as a complementary tool to facilitate data access, processing and analysing, but requiring a tool for SDMX metadata management, and a system for storing data.
FMR is a natural candidate for this kind of use. Because FMR offers a REST API, not only to serve metadata, but also to perform actions, the integration between SDMXThon and FMR is quite simple, even if they are built using different technologies.
The comprehensive example in next section shows how FMR can be used together with SDMXThon.
