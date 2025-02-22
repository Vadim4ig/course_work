PGDMP          
             }            inventorybd    16.6    16.6 O    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16401    inventorybd    DATABASE        CREATE DATABASE inventorybd WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE inventorybd;
                inventorybd    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    24631 	   customers    TABLE     �   CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    name character varying(255),
    email character varying(255),
    phone character varying(20),
    address character varying(255)
);
    DROP TABLE public.customers;
       public         heap    inventorybd    false    4            �            1259    24630    customers_customer_id_seq    SEQUENCE     �   CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.customers_customer_id_seq;
       public          inventorybd    false    224    4            �           0    0    customers_customer_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;
          public          inventorybd    false    223            �            1259    24613    events    TABLE     �   CREATE TABLE public.events (
    event_id integer NOT NULL,
    event_type character varying(50),
    product_id integer,
    quantity integer,
    event_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    supplier_id integer
);
    DROP TABLE public.events;
       public         heap    inventorybd    false    4            �            1259    24612    events_event_id_seq    SEQUENCE     �   CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.events_event_id_seq;
       public          inventorybd    false    222    4            �           0    0    events_event_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;
          public          inventorybd    false    221            �            1259    24658 	   favorites    TABLE     �   CREATE TABLE public.favorites (
    favorite_id integer NOT NULL,
    customer_id integer,
    product_id integer,
    added_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.favorites;
       public         heap    inventorybd    false    4            �            1259    24657    favorites_favorite_id_seq    SEQUENCE     �   CREATE SEQUENCE public.favorites_favorite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.favorites_favorite_id_seq;
       public          inventorybd    false    228    4            �           0    0    favorites_favorite_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.favorites_favorite_id_seq OWNED BY public.favorites.favorite_id;
          public          inventorybd    false    227            �            1259    24600 	   inventory    TABLE     �   CREATE TABLE public.inventory (
    inventory_id integer NOT NULL,
    product_id integer,
    quantity_in_stock integer,
    last_updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.inventory;
       public         heap    inventorybd    false    4            �            1259    24599    inventory_inventory_id_seq    SEQUENCE     �   CREATE SEQUENCE public.inventory_inventory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.inventory_inventory_id_seq;
       public          inventorybd    false    4    220            �           0    0    inventory_inventory_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.inventory_inventory_id_seq OWNED BY public.inventory.inventory_id;
          public          inventorybd    false    219            �            1259    24586    products    TABLE       CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name character varying(255),
    product_type character varying(255),
    color character varying(50),
    size character varying(50),
    price numeric(10,2),
    supplier_id integer
);
    DROP TABLE public.products;
       public         heap    inventorybd    false    4            �            1259    24585    products_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.products_product_id_seq;
       public          inventorybd    false    218    4            �           0    0    products_product_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;
          public          inventorybd    false    217            �            1259    24676    sales    TABLE     �   CREATE TABLE public.sales (
    sale_id integer NOT NULL,
    customer_id integer,
    product_id integer,
    quantity integer,
    total_price numeric(10,2),
    sale_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.sales;
       public         heap    inventorybd    false    4            �            1259    24675    sales_sale_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sales_sale_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.sales_sale_id_seq;
       public          inventorybd    false    4    230            �           0    0    sales_sale_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.sales_sale_id_seq OWNED BY public.sales.sale_id;
          public          inventorybd    false    229            �            1259    24640    shopping_cart    TABLE     �   CREATE TABLE public.shopping_cart (
    cart_id integer NOT NULL,
    customer_id integer,
    product_id integer,
    quantity integer,
    added_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
 !   DROP TABLE public.shopping_cart;
       public         heap    inventorybd    false    4            �            1259    24639    shopping_cart_cart_id_seq    SEQUENCE     �   CREATE SEQUENCE public.shopping_cart_cart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.shopping_cart_cart_id_seq;
       public          inventorybd    false    226    4            �           0    0    shopping_cart_cart_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.shopping_cart_cart_id_seq OWNED BY public.shopping_cart.cart_id;
          public          inventorybd    false    225            �            1259    24577 	   suppliers    TABLE     �   CREATE TABLE public.suppliers (
    supplier_id integer NOT NULL,
    name character varying(255),
    contact_name character varying(255),
    phone character varying(20),
    address character varying(255)
);
    DROP TABLE public.suppliers;
       public         heap    inventorybd    false    4            �            1259    24576    suppliers_supplier_id_seq    SEQUENCE     �   CREATE SEQUENCE public.suppliers_supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.suppliers_supplier_id_seq;
       public          inventorybd    false    4    216            �           0    0    suppliers_supplier_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.suppliers_supplier_id_seq OWNED BY public.suppliers.supplier_id;
          public          inventorybd    false    215            �            1259    24694 
   user_roles    TABLE     |   CREATE TABLE public.user_roles (
    role_id integer NOT NULL,
    role_name character varying(50),
    permissions text
);
    DROP TABLE public.user_roles;
       public         heap    inventorybd    false    4            �            1259    24693    user_roles_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.user_roles_role_id_seq;
       public          inventorybd    false    232    4            �           0    0    user_roles_role_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.user_roles_role_id_seq OWNED BY public.user_roles.role_id;
          public          inventorybd    false    231            *           2604    24634    customers customer_id    DEFAULT     ~   ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);
 D   ALTER TABLE public.customers ALTER COLUMN customer_id DROP DEFAULT;
       public          inventorybd    false    223    224    224            (           2604    24616    events event_id    DEFAULT     r   ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);
 >   ALTER TABLE public.events ALTER COLUMN event_id DROP DEFAULT;
       public          inventorybd    false    222    221    222            -           2604    24661    favorites favorite_id    DEFAULT     ~   ALTER TABLE ONLY public.favorites ALTER COLUMN favorite_id SET DEFAULT nextval('public.favorites_favorite_id_seq'::regclass);
 D   ALTER TABLE public.favorites ALTER COLUMN favorite_id DROP DEFAULT;
       public          inventorybd    false    228    227    228            &           2604    24603    inventory inventory_id    DEFAULT     �   ALTER TABLE ONLY public.inventory ALTER COLUMN inventory_id SET DEFAULT nextval('public.inventory_inventory_id_seq'::regclass);
 E   ALTER TABLE public.inventory ALTER COLUMN inventory_id DROP DEFAULT;
       public          inventorybd    false    219    220    220            %           2604    24589    products product_id    DEFAULT     z   ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);
 B   ALTER TABLE public.products ALTER COLUMN product_id DROP DEFAULT;
       public          inventorybd    false    217    218    218            /           2604    24679    sales sale_id    DEFAULT     n   ALTER TABLE ONLY public.sales ALTER COLUMN sale_id SET DEFAULT nextval('public.sales_sale_id_seq'::regclass);
 <   ALTER TABLE public.sales ALTER COLUMN sale_id DROP DEFAULT;
       public          inventorybd    false    230    229    230            +           2604    24643    shopping_cart cart_id    DEFAULT     ~   ALTER TABLE ONLY public.shopping_cart ALTER COLUMN cart_id SET DEFAULT nextval('public.shopping_cart_cart_id_seq'::regclass);
 D   ALTER TABLE public.shopping_cart ALTER COLUMN cart_id DROP DEFAULT;
       public          inventorybd    false    225    226    226            $           2604    24580    suppliers supplier_id    DEFAULT     ~   ALTER TABLE ONLY public.suppliers ALTER COLUMN supplier_id SET DEFAULT nextval('public.suppliers_supplier_id_seq'::regclass);
 D   ALTER TABLE public.suppliers ALTER COLUMN supplier_id DROP DEFAULT;
       public          inventorybd    false    216    215    216            1           2604    24697    user_roles role_id    DEFAULT     x   ALTER TABLE ONLY public.user_roles ALTER COLUMN role_id SET DEFAULT nextval('public.user_roles_role_id_seq'::regclass);
 A   ALTER TABLE public.user_roles ALTER COLUMN role_id DROP DEFAULT;
       public          inventorybd    false    231    232    232            �          0    24631 	   customers 
   TABLE DATA           M   COPY public.customers (customer_id, name, email, phone, address) FROM stdin;
    public          inventorybd    false    224   2_       �          0    24613    events 
   TABLE DATA           e   COPY public.events (event_id, event_type, product_id, quantity, event_date, supplier_id) FROM stdin;
    public          inventorybd    false    222   O_       �          0    24658 	   favorites 
   TABLE DATA           U   COPY public.favorites (favorite_id, customer_id, product_id, added_date) FROM stdin;
    public          inventorybd    false    228   l_       �          0    24600 	   inventory 
   TABLE DATA           ^   COPY public.inventory (inventory_id, product_id, quantity_in_stock, last_updated) FROM stdin;
    public          inventorybd    false    220   �_       �          0    24586    products 
   TABLE DATA           k   COPY public.products (product_id, product_name, product_type, color, size, price, supplier_id) FROM stdin;
    public          inventorybd    false    218   �_       �          0    24676    sales 
   TABLE DATA           c   COPY public.sales (sale_id, customer_id, product_id, quantity, total_price, sale_date) FROM stdin;
    public          inventorybd    false    230   �_       �          0    24640    shopping_cart 
   TABLE DATA           _   COPY public.shopping_cart (cart_id, customer_id, product_id, quantity, added_date) FROM stdin;
    public          inventorybd    false    226   �_       �          0    24577 	   suppliers 
   TABLE DATA           T   COPY public.suppliers (supplier_id, name, contact_name, phone, address) FROM stdin;
    public          inventorybd    false    216   �_       �          0    24694 
   user_roles 
   TABLE DATA           E   COPY public.user_roles (role_id, role_name, permissions) FROM stdin;
    public          inventorybd    false    232   `       �           0    0    customers_customer_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.customers_customer_id_seq', 1, false);
          public          inventorybd    false    223                        0    0    events_event_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.events_event_id_seq', 1, false);
          public          inventorybd    false    221                       0    0    favorites_favorite_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.favorites_favorite_id_seq', 1, false);
          public          inventorybd    false    227                       0    0    inventory_inventory_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.inventory_inventory_id_seq', 1, false);
          public          inventorybd    false    219                       0    0    products_product_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.products_product_id_seq', 1, false);
          public          inventorybd    false    217                       0    0    sales_sale_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.sales_sale_id_seq', 1, false);
          public          inventorybd    false    229                       0    0    shopping_cart_cart_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.shopping_cart_cart_id_seq', 1, false);
          public          inventorybd    false    225                       0    0    suppliers_supplier_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.suppliers_supplier_id_seq', 1, false);
          public          inventorybd    false    215                       0    0    user_roles_role_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.user_roles_role_id_seq', 1, false);
          public          inventorybd    false    231            ;           2606    24638    customers customers_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);
 B   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_pkey;
       public            inventorybd    false    224            9           2606    24619    events events_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);
 <   ALTER TABLE ONLY public.events DROP CONSTRAINT events_pkey;
       public            inventorybd    false    222            ?           2606    24664    favorites favorites_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (favorite_id);
 B   ALTER TABLE ONLY public.favorites DROP CONSTRAINT favorites_pkey;
       public            inventorybd    false    228            7           2606    24606    inventory inventory_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (inventory_id);
 B   ALTER TABLE ONLY public.inventory DROP CONSTRAINT inventory_pkey;
       public            inventorybd    false    220            5           2606    24593    products products_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public            inventorybd    false    218            A           2606    24682    sales sales_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (sale_id);
 :   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_pkey;
       public            inventorybd    false    230            =           2606    24646     shopping_cart shopping_cart_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.shopping_cart
    ADD CONSTRAINT shopping_cart_pkey PRIMARY KEY (cart_id);
 J   ALTER TABLE ONLY public.shopping_cart DROP CONSTRAINT shopping_cart_pkey;
       public            inventorybd    false    226            3           2606    24584    suppliers suppliers_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id);
 B   ALTER TABLE ONLY public.suppliers DROP CONSTRAINT suppliers_pkey;
       public            inventorybd    false    216            C           2606    24701    user_roles user_roles_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (role_id);
 D   ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_pkey;
       public            inventorybd    false    232            F           2606    24620    events events_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);
 G   ALTER TABLE ONLY public.events DROP CONSTRAINT events_product_id_fkey;
       public          inventorybd    false    222    4661    218            G           2606    24625    events events_supplier_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplier_id);
 H   ALTER TABLE ONLY public.events DROP CONSTRAINT events_supplier_id_fkey;
       public          inventorybd    false    4659    222    216            J           2606    24665 $   favorites favorites_customer_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);
 N   ALTER TABLE ONLY public.favorites DROP CONSTRAINT favorites_customer_id_fkey;
       public          inventorybd    false    228    4667    224            K           2606    24670 #   favorites favorites_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);
 M   ALTER TABLE ONLY public.favorites DROP CONSTRAINT favorites_product_id_fkey;
       public          inventorybd    false    228    4661    218            E           2606    24607 #   inventory inventory_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);
 M   ALTER TABLE ONLY public.inventory DROP CONSTRAINT inventory_product_id_fkey;
       public          inventorybd    false    4661    220    218            D           2606    24594 "   products products_supplier_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.suppliers(supplier_id);
 L   ALTER TABLE ONLY public.products DROP CONSTRAINT products_supplier_id_fkey;
       public          inventorybd    false    218    4659    216            L           2606    24683    sales sales_customer_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);
 F   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_customer_id_fkey;
       public          inventorybd    false    4667    224    230            M           2606    24688    sales sales_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);
 E   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_product_id_fkey;
       public          inventorybd    false    218    230    4661            H           2606    24647 ,   shopping_cart shopping_cart_customer_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.shopping_cart
    ADD CONSTRAINT shopping_cart_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);
 V   ALTER TABLE ONLY public.shopping_cart DROP CONSTRAINT shopping_cart_customer_id_fkey;
       public          inventorybd    false    226    4667    224            I           2606    24652 +   shopping_cart shopping_cart_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.shopping_cart
    ADD CONSTRAINT shopping_cart_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id);
 U   ALTER TABLE ONLY public.shopping_cart DROP CONSTRAINT shopping_cart_product_id_fkey;
       public          inventorybd    false    4661    218    226            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     