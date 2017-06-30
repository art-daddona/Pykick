--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Name: blade_info_blade_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE blade_info_blade_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE blade_info_blade_fk_seq OWNER TO art;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: blade_info; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE blade_info (
    blade_fk integer DEFAULT nextval('blade_info_blade_fk_seq'::regclass) NOT NULL,
    global_fk integer NOT NULL,
    server_fk integer NOT NULL,
    blade_center integer NOT NULL,
    unit integer NOT NULL,
    serial_number character varying(256) NOT NULL,
    blade_center_ip_v4 character varying(15) NOT NULL,
    ipmi_ip_v4 character varying(15) NOT NULL
);


ALTER TABLE blade_info OWNER TO art;

--
-- Name: globals; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE globals (
    global_fk integer NOT NULL,
    global_name character varying(64) NOT NULL,
    dhcpd_ip character varying(15) NOT NULL,
    dhcpd_path character varying(1024) NOT NULL,
    tftpd_ip character varying(15) NOT NULL,
    tftpd_path character varying(1024) NOT NULL,
    http_ip character varying(15) NOT NULL,
    http_top character varying(1024) NOT NULL,
    os_path character varying(1024) NOT NULL,
    scripts_path character varying(1024) NOT NULL,
    templates_path character varying(1024) NOT NULL,
    software_path character varying(1024) NOT NULL,
    vm_path character varying(1024) NOT NULL,
    openstack_path character varying(1024) NOT NULL,
    keyboard character varying(64) NOT NULL,
    timezone character varying(64) NOT NULL,
    root_pw character varying(256) NOT NULL,
    default_user character varying(256) NOT NULL,
    default_user_pw character varying(256) NOT NULL,
    dns_servers character varying(1024) NOT NULL,
    ntp_servers character varying(1024) NOT NULL,
    domain character varying(256) NOT NULL,
    search_domains character varying(1024) NOT NULL,
    log_server character varying(15) NOT NULL,
    nagios_server character varying(15) NOT NULL
);


ALTER TABLE globals OWNER TO art;

--
-- Name: globals_global_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE globals_global_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE globals_global_fk_seq OWNER TO art;

--
-- Name: globals_global_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE globals_global_fk_seq OWNED BY globals.global_fk;


--
-- Name: openstack_info; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE openstack_info (
    openstack_fk integer NOT NULL,
    global_fk integer NOT NULL,
    server_fk integer NOT NULL,
    openstack_url character varying(1024),
    image character varying(256),
    flavor character varying(256),
    management_network character varying(256),
    application_network character varying(256),
    ssh_key character varying(256),
    security_group character varying(256),
    zone character varying
);


ALTER TABLE openstack_info OWNER TO art;

--
-- Name: openstack_info_openstack_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE openstack_info_openstack_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE openstack_info_openstack_fk_seq OWNER TO art;

--
-- Name: openstack_info_openstack_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE openstack_info_openstack_fk_seq OWNED BY openstack_info.openstack_fk;


--
-- Name: rack_info; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE rack_info (
    rack_fk integer NOT NULL,
    global_fk integer NOT NULL,
    server_fk integer NOT NULL,
    building character varying(256) NOT NULL,
    floor integer NOT NULL,
    "row" integer NOT NULL,
    rack integer NOT NULL,
    unit integer NOT NULL,
    size integer NOT NULL,
    serial_number character varying(256) NOT NULL,
    ipmi_ip_v4 character varying(15) NOT NULL
);


ALTER TABLE rack_info OWNER TO art;

--
-- Name: rack_info_rack_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE rack_info_rack_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE rack_info_rack_fk_seq OWNER TO art;

--
-- Name: rack_info_rack_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE rack_info_rack_fk_seq OWNED BY rack_info.rack_fk;


--
-- Name: servers; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE servers (
    server_fk integer NOT NULL,
    global_fk integer NOT NULL,
    hostname character varying(64) NOT NULL,
    os_version character varying(64) NOT NULL,
    drive character varying(64) NOT NULL,
    swap integer NOT NULL,
    console_port integer NOT NULL,
    console_speed integer NOT NULL,
    pxe_mac character varying(17) NOT NULL,
    pxe_device character varying(64) NOT NULL,
    management_device character varying(64) NOT NULL,
    management_ip_v4 character varying(15) NOT NULL,
    management_ip_v6 character varying(256) NOT NULL,
    application_device character varying(64) NOT NULL,
    application_ip_v4 character varying(15) NOT NULL,
    application_ip_v6 character varying(64) NOT NULL,
    domain character varying(256) NOT NULL,
    application_type character varying(64) NOT NULL,
    system_type character varying(64) NOT NULL,
    status character varying(64) NOT NULL
);


ALTER TABLE servers OWNER TO art;

--
-- Name: servers_server_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE servers_server_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE servers_server_fk_seq OWNER TO art;

--
-- Name: servers_server_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE servers_server_fk_seq OWNED BY servers.server_fk;


--
-- Name: subnet_v4; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE subnet_v4 (
    subnet_v4_fk integer NOT NULL,
    global_fk integer NOT NULL,
    subnet_name character varying(256) NOT NULL,
    subnet_description character varying(1024) NOT NULL,
    subnet_network character varying(15) NOT NULL,
    subnet_netmask character varying(15) NOT NULL,
    subnet_router character varying(15) NOT NULL,
    subnet_dhcp integer NOT NULL
);


ALTER TABLE subnet_v4 OWNER TO art;

--
-- Name: subnet_v4_subnet_v4_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE subnet_v4_subnet_v4_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subnet_v4_subnet_v4_fk_seq OWNER TO art;

--
-- Name: subnet_v4_subnet_v4_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE subnet_v4_subnet_v4_fk_seq OWNED BY subnet_v4.subnet_v4_fk;


--
-- Name: subnet_v6; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE subnet_v6 (
    subnet_v6_fk integer NOT NULL,
    global_fk integer NOT NULL,
    subnet_name character varying(64) NOT NULL,
    subnet_description character varying(256) NOT NULL,
    subnet_network character varying(40) NOT NULL,
    subnet_netmask character varying(4) NOT NULL,
    subnet_router character varying(40) NOT NULL,
    subnet_dhcp integer NOT NULL
);


ALTER TABLE subnet_v6 OWNER TO art;

--
-- Name: subnet_v6_subnet_v6_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE subnet_v6_subnet_v6_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subnet_v6_subnet_v6_fk_seq OWNER TO art;

--
-- Name: subnet_v6_subnet_v6_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE subnet_v6_subnet_v6_fk_seq OWNED BY subnet_v6.subnet_v6_fk;


--
-- Name: vm_info; Type: TABLE; Schema: public; Owner: art; Tablespace: 
--

CREATE TABLE vm_info (
    vm_fk integer NOT NULL,
    global_fk integer NOT NULL,
    server_fk integer NOT NULL,
    vm_type character varying(64) NOT NULL,
    vm_host character varying(1024) NOT NULL,
    vm_rdp_port integer NOT NULL,
    vm_memory integer NOT NULL,
    vm_cpu integer NOT NULL,
    vm_interface_device character varying(256) NOT NULL,
    vm_drive_type character varying(256) NOT NULL,
    vm_iscsi_target character varying(40),
    vm_iscsi_port integer,
    vm_iscsi_iqn character varying(256)
);


ALTER TABLE vm_info OWNER TO art;

--
-- Name: vm_info_vm_fk_seq; Type: SEQUENCE; Schema: public; Owner: art
--

CREATE SEQUENCE vm_info_vm_fk_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE vm_info_vm_fk_seq OWNER TO art;

--
-- Name: vm_info_vm_fk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: art
--

ALTER SEQUENCE vm_info_vm_fk_seq OWNED BY vm_info.vm_fk;


--
-- Name: global_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY globals ALTER COLUMN global_fk SET DEFAULT nextval('globals_global_fk_seq'::regclass);


--
-- Name: openstack_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY openstack_info ALTER COLUMN openstack_fk SET DEFAULT nextval('openstack_info_openstack_fk_seq'::regclass);


--
-- Name: rack_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY rack_info ALTER COLUMN rack_fk SET DEFAULT nextval('rack_info_rack_fk_seq'::regclass);


--
-- Name: server_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY servers ALTER COLUMN server_fk SET DEFAULT nextval('servers_server_fk_seq'::regclass);


--
-- Name: subnet_v4_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY subnet_v4 ALTER COLUMN subnet_v4_fk SET DEFAULT nextval('subnet_v4_subnet_v4_fk_seq'::regclass);


--
-- Name: subnet_v6_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY subnet_v6 ALTER COLUMN subnet_v6_fk SET DEFAULT nextval('subnet_v6_subnet_v6_fk_seq'::regclass);


--
-- Name: vm_fk; Type: DEFAULT; Schema: public; Owner: art
--

ALTER TABLE ONLY vm_info ALTER COLUMN vm_fk SET DEFAULT nextval('vm_info_vm_fk_seq'::regclass);


--
-- Name: blade_info_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY blade_info
    ADD CONSTRAINT blade_info_pkey PRIMARY KEY (blade_fk);


--
-- Name: blade_info_server_fk_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY blade_info
    ADD CONSTRAINT blade_info_server_fk_key UNIQUE (server_fk);


--
-- Name: globals_global_name_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY globals
    ADD CONSTRAINT globals_global_name_key UNIQUE (global_name);


--
-- Name: globals_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY globals
    ADD CONSTRAINT globals_pkey PRIMARY KEY (global_fk);


--
-- Name: rack_info_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY rack_info
    ADD CONSTRAINT rack_info_pkey PRIMARY KEY (rack_fk);


--
-- Name: rack_info_server_fk_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY rack_info
    ADD CONSTRAINT rack_info_server_fk_key UNIQUE (server_fk);


--
-- Name: servers_hostname_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY servers
    ADD CONSTRAINT servers_hostname_key UNIQUE (hostname);


--
-- Name: servers_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY servers
    ADD CONSTRAINT servers_pkey PRIMARY KEY (server_fk);


--
-- Name: servers_pxe_mac_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY servers
    ADD CONSTRAINT servers_pxe_mac_key UNIQUE (pxe_mac);


--
-- Name: subnet_v4_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v4
    ADD CONSTRAINT subnet_v4_pkey PRIMARY KEY (subnet_v4_fk);


--
-- Name: subnet_v4_subnet_name_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v4
    ADD CONSTRAINT subnet_v4_subnet_name_key UNIQUE (subnet_name);


--
-- Name: subnet_v4_subnet_network_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v4
    ADD CONSTRAINT subnet_v4_subnet_network_key UNIQUE (subnet_network);


--
-- Name: subnet_v4_subnet_router_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v4
    ADD CONSTRAINT subnet_v4_subnet_router_key UNIQUE (subnet_router);


--
-- Name: subnet_v6_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v6
    ADD CONSTRAINT subnet_v6_pkey PRIMARY KEY (subnet_v6_fk);


--
-- Name: subnet_v6_subnet_name_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v6
    ADD CONSTRAINT subnet_v6_subnet_name_key UNIQUE (subnet_name);


--
-- Name: subnet_v6_subnet_network_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v6
    ADD CONSTRAINT subnet_v6_subnet_network_key UNIQUE (subnet_network);


--
-- Name: subnet_v6_subnet_router_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY subnet_v6
    ADD CONSTRAINT subnet_v6_subnet_router_key UNIQUE (subnet_router);


--
-- Name: vm_info_pkey; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY vm_info
    ADD CONSTRAINT vm_info_pkey PRIMARY KEY (vm_fk);


--
-- Name: vm_info_server_fk_key; Type: CONSTRAINT; Schema: public; Owner: art; Tablespace: 
--

ALTER TABLE ONLY vm_info
    ADD CONSTRAINT vm_info_server_fk_key UNIQUE (server_fk);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

