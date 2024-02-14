PGDMP                      |         
   biblioteca    16.1    16.1 5    4           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            5           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            6           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            7           1262    25142 
   biblioteca    DATABASE     �   CREATE DATABASE biblioteca WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE biblioteca;
                postgres    false            �            1255    25143    fn_prestamos()    FUNCTION     5  CREATE FUNCTION public.fn_prestamos() RETURNS TABLE(cod_prestamo integer, dni integer, cod_bibliotecario integer, fecha_entrega text, fecha_devolucion text, cliente text, bibliotecario text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY 
    SELECT pr.cod_prestamo,
           pr.dni,
           pr.cod_bibliotecario,
           to_char(pr.fecha_entrega::timestamp with time zone, 'yyyy-mm-dd'::text) AS fecha_entrega,
		   to_char(pr.fecha_devolucion::timestamp with time zone, 'yyyy-mm-dd'::text) AS fecha_devolucion,
           (pe.apellido_p || ' ' || pe.apellido_m || ' ' || pe.nombre) as cliente,
           (b.apellido_p || ' ' || b.apellido_m || ' ' || b.nombre) as bibliotecario
    FROM prestamo_cab pr
    JOIN persona pe ON pe.dni = pr.dni
    JOIN persona b ON b.dni = pr.cod_bibliotecario;
END;
$$;
 %   DROP FUNCTION public.fn_prestamos();
       public          postgres    false            �            1255    25144    obtener_libros_disponibles()    FUNCTION     �  CREATE FUNCTION public.obtener_libros_disponibles() RETURNS TABLE(cod_libro integer, titulo character varying, autor character varying, stock integer, stock_disponible integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY 
   SELECT
    l.cod_libro,
    l.titulo,
    l.autor,
	l.stock,
    (l.stock - COALESCE((SELECT COUNT(*) FROM prestamo_det pd WHERE prestado and pd.cod_libro = l.cod_libro), 0))::integer AS stock_disponible
FROM 
    libro l
WHERE
    l.stock > 0;
END;
$$;
 3   DROP FUNCTION public.obtener_libros_disponibles();
       public          postgres    false            �            1259    25145    libro    TABLE     �   CREATE TABLE public.libro (
    cod_libro integer NOT NULL,
    titulo character varying(50) NOT NULL,
    materia character varying(50) NOT NULL,
    autor character varying(50) NOT NULL,
    descripcion text,
    stock integer DEFAULT 0 NOT NULL
);
    DROP TABLE public.libro;
       public         heap    postgres    false            �            1259    25151    libro_cod_libro_seq    SEQUENCE     �   CREATE SEQUENCE public.libro_cod_libro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.libro_cod_libro_seq;
       public          postgres    false    215            8           0    0    libro_cod_libro_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.libro_cod_libro_seq OWNED BY public.libro.cod_libro;
          public          postgres    false    216            �            1259    25152    persona    TABLE     �   CREATE TABLE public.persona (
    dni integer NOT NULL,
    nombre character varying(50),
    apellido_p character varying(50),
    apellido_m character varying(50)
);
    DROP TABLE public.persona;
       public         heap    postgres    false            �            1259    25155    persona_rol    TABLE     \   CREATE TABLE public.persona_rol (
    dni integer NOT NULL,
    cod_rol integer NOT NULL
);
    DROP TABLE public.persona_rol;
       public         heap    postgres    false            �            1259    25158    rol    TABLE     e   CREATE TABLE public.rol (
    cod_rol integer NOT NULL,
    nombre character varying(20) NOT NULL
);
    DROP TABLE public.rol;
       public         heap    postgres    false            �            1259    25161    lista_persona_rol    VIEW     w  CREATE VIEW public.lista_persona_rol AS
 SELECT p.dni,
    p.nombre,
    p.apellido_p,
    p.apellido_m,
    r.nombre AS rol,
    (((((p.nombre)::text || ' '::text) || (p.apellido_p)::text) || ' '::text) || (p.apellido_m)::text) AS datos
   FROM ((public.persona p
     JOIN public.persona_rol pr ON ((pr.dni = p.dni)))
     JOIN public.rol r ON ((r.cod_rol = pr.cod_rol)));
 $   DROP VIEW public.lista_persona_rol;
       public          postgres    false    217    217    219    217    217    219    218    218            �            1259    25165    prestamo_cab    TABLE     �   CREATE TABLE public.prestamo_cab (
    cod_prestamo integer NOT NULL,
    dni integer,
    cod_bibliotecario integer,
    fecha_entrega date,
    fecha_devolucion date
);
     DROP TABLE public.prestamo_cab;
       public         heap    postgres    false            �            1259    25168    prestamo_det    TABLE     �   CREATE TABLE public.prestamo_det (
    cod_prestamo_det integer NOT NULL,
    cod_prestamo integer NOT NULL,
    cod_libro integer NOT NULL,
    prestado boolean DEFAULT true NOT NULL
);
     DROP TABLE public.prestamo_det;
       public         heap    postgres    false            �            1259    25172    lista_prestamos    VIEW     �  CREATE VIEW public.lista_prestamos AS
 SELECT (((((pe.nombre)::text || ' '::text) || (pe.apellido_p)::text) || ' '::text) || (pe.apellido_m)::text) AS usuario,
    p.cod_prestamo_det,
    p.cod_prestamo,
    p.cod_libro,
    l.titulo AS libro,
    p.prestado
   FROM (((public.prestamo_det p
     JOIN public.libro l ON ((l.cod_libro = p.cod_libro)))
     JOIN public.prestamo_cab pc ON ((pc.cod_prestamo = p.cod_prestamo)))
     JOIN public.persona pe ON ((pe.dni = pc.dni)));
 "   DROP VIEW public.lista_prestamos;
       public          postgres    false    215    222    222    222    222    221    221    217    217    217    217    215            �            1259    25177    login    TABLE     �   CREATE TABLE public.login (
    dni integer NOT NULL,
    usuario character varying(20) NOT NULL,
    clave character varying(100) NOT NULL
);
    DROP TABLE public.login;
       public         heap    postgres    false            �            1259    25180    lista_usuarios    VIEW     <  CREATE VIEW public.lista_usuarios AS
 SELECT l.dni,
    l.usuario,
    l.clave,
    p.nombre,
    p.apellido_p,
    p.apellido_m,
    (((((p.nombre)::text || ' '::text) || (p.apellido_p)::text) || ' '::text) || (p.apellido_m)::text) AS datos
   FROM (public.login l
     JOIN public.persona p ON ((p.dni = l.dni)));
 !   DROP VIEW public.lista_usuarios;
       public          postgres    false    224    217    224    224    217    217    217            �            1259    25184    prestamo_cab_cod_prestamo_seq    SEQUENCE     �   CREATE SEQUENCE public.prestamo_cab_cod_prestamo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.prestamo_cab_cod_prestamo_seq;
       public          postgres    false    221            9           0    0    prestamo_cab_cod_prestamo_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.prestamo_cab_cod_prestamo_seq OWNED BY public.prestamo_cab.cod_prestamo;
          public          postgres    false    226            �            1259    25185 !   prestamo_det_cod_prestamo_det_seq    SEQUENCE     �   CREATE SEQUENCE public.prestamo_det_cod_prestamo_det_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.prestamo_det_cod_prestamo_det_seq;
       public          postgres    false    222            :           0    0 !   prestamo_det_cod_prestamo_det_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.prestamo_det_cod_prestamo_det_seq OWNED BY public.prestamo_det.cod_prestamo_det;
          public          postgres    false    227            �            1259    25186    rol_cod_rol_seq    SEQUENCE     �   CREATE SEQUENCE public.rol_cod_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.rol_cod_rol_seq;
       public          postgres    false    219            ;           0    0    rol_cod_rol_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.rol_cod_rol_seq OWNED BY public.rol.cod_rol;
          public          postgres    false    228            y           2604    25187    libro cod_libro    DEFAULT     r   ALTER TABLE ONLY public.libro ALTER COLUMN cod_libro SET DEFAULT nextval('public.libro_cod_libro_seq'::regclass);
 >   ALTER TABLE public.libro ALTER COLUMN cod_libro DROP DEFAULT;
       public          postgres    false    216    215            |           2604    25188    prestamo_cab cod_prestamo    DEFAULT     �   ALTER TABLE ONLY public.prestamo_cab ALTER COLUMN cod_prestamo SET DEFAULT nextval('public.prestamo_cab_cod_prestamo_seq'::regclass);
 H   ALTER TABLE public.prestamo_cab ALTER COLUMN cod_prestamo DROP DEFAULT;
       public          postgres    false    226    221            }           2604    25189    prestamo_det cod_prestamo_det    DEFAULT     �   ALTER TABLE ONLY public.prestamo_det ALTER COLUMN cod_prestamo_det SET DEFAULT nextval('public.prestamo_det_cod_prestamo_det_seq'::regclass);
 L   ALTER TABLE public.prestamo_det ALTER COLUMN cod_prestamo_det DROP DEFAULT;
       public          postgres    false    227    222            {           2604    25190    rol cod_rol    DEFAULT     j   ALTER TABLE ONLY public.rol ALTER COLUMN cod_rol SET DEFAULT nextval('public.rol_cod_rol_seq'::regclass);
 :   ALTER TABLE public.rol ALTER COLUMN cod_rol DROP DEFAULT;
       public          postgres    false    228    219            '          0    25145    libro 
   TABLE DATA           V   COPY public.libro (cod_libro, titulo, materia, autor, descripcion, stock) FROM stdin;
    public          postgres    false    215   uE       .          0    25177    login 
   TABLE DATA           4   COPY public.login (dni, usuario, clave) FROM stdin;
    public          postgres    false    224   �F       )          0    25152    persona 
   TABLE DATA           F   COPY public.persona (dni, nombre, apellido_p, apellido_m) FROM stdin;
    public          postgres    false    217   cG       *          0    25155    persona_rol 
   TABLE DATA           3   COPY public.persona_rol (dni, cod_rol) FROM stdin;
    public          postgres    false    218   
H       ,          0    25165    prestamo_cab 
   TABLE DATA           m   COPY public.prestamo_cab (cod_prestamo, dni, cod_bibliotecario, fecha_entrega, fecha_devolucion) FROM stdin;
    public          postgres    false    221   8H       -          0    25168    prestamo_det 
   TABLE DATA           [   COPY public.prestamo_det (cod_prestamo_det, cod_prestamo, cod_libro, prestado) FROM stdin;
    public          postgres    false    222   �H       +          0    25158    rol 
   TABLE DATA           .   COPY public.rol (cod_rol, nombre) FROM stdin;
    public          postgres    false    219   ,I       <           0    0    libro_cod_libro_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.libro_cod_libro_seq', 11, true);
          public          postgres    false    216            =           0    0    prestamo_cab_cod_prestamo_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.prestamo_cab_cod_prestamo_seq', 17, true);
          public          postgres    false    226            >           0    0 !   prestamo_det_cod_prestamo_det_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.prestamo_det_cod_prestamo_det_seq', 25, true);
          public          postgres    false    227            ?           0    0    rol_cod_rol_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.rol_cod_rol_seq', 9, true);
          public          postgres    false    228            �           2606    25192    libro libro_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.libro
    ADD CONSTRAINT libro_pkey PRIMARY KEY (cod_libro);
 :   ALTER TABLE ONLY public.libro DROP CONSTRAINT libro_pkey;
       public            postgres    false    215            �           2606    25194    login login_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY (dni);
 :   ALTER TABLE ONLY public.login DROP CONSTRAINT login_pkey;
       public            postgres    false    224            �           2606    25196    login login_uk 
   CONSTRAINT     L   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_uk UNIQUE (usuario);
 8   ALTER TABLE ONLY public.login DROP CONSTRAINT login_uk;
       public            postgres    false    224            �           2606    25198    persona persona_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.persona
    ADD CONSTRAINT persona_pkey PRIMARY KEY (dni);
 >   ALTER TABLE ONLY public.persona DROP CONSTRAINT persona_pkey;
       public            postgres    false    217            �           2606    25200    persona_rol persona_rol_uk 
   CONSTRAINT     ]   ALTER TABLE ONLY public.persona_rol
    ADD CONSTRAINT persona_rol_uk UNIQUE (dni, cod_rol);
 D   ALTER TABLE ONLY public.persona_rol DROP CONSTRAINT persona_rol_uk;
       public            postgres    false    218    218            �           2606    25202    prestamo_cab prestamo_cab_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.prestamo_cab
    ADD CONSTRAINT prestamo_cab_pkey PRIMARY KEY (cod_prestamo);
 H   ALTER TABLE ONLY public.prestamo_cab DROP CONSTRAINT prestamo_cab_pkey;
       public            postgres    false    221            �           2606    25204    prestamo_det prestamo_det_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.prestamo_det
    ADD CONSTRAINT prestamo_det_pkey PRIMARY KEY (cod_prestamo_det);
 H   ALTER TABLE ONLY public.prestamo_det DROP CONSTRAINT prestamo_det_pkey;
       public            postgres    false    222            �           2606    25206    rol rol_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (cod_rol);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    219            �           2606    25207 $   persona_rol persona_rol_cod_rol_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.persona_rol
    ADD CONSTRAINT persona_rol_cod_rol_fkey FOREIGN KEY (cod_rol) REFERENCES public.rol(cod_rol);
 N   ALTER TABLE ONLY public.persona_rol DROP CONSTRAINT persona_rol_cod_rol_fkey;
       public          postgres    false    219    4742    218            �           2606    25212     persona_rol persona_rol_dni_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.persona_rol
    ADD CONSTRAINT persona_rol_dni_fkey FOREIGN KEY (dni) REFERENCES public.persona(dni);
 J   ALTER TABLE ONLY public.persona_rol DROP CONSTRAINT persona_rol_dni_fkey;
       public          postgres    false    217    4738    218            �           2606    25217 0   prestamo_cab prestamo_cab_cod_bibliotecario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prestamo_cab
    ADD CONSTRAINT prestamo_cab_cod_bibliotecario_fkey FOREIGN KEY (cod_bibliotecario) REFERENCES public.persona(dni);
 Z   ALTER TABLE ONLY public.prestamo_cab DROP CONSTRAINT prestamo_cab_cod_bibliotecario_fkey;
       public          postgres    false    4738    221    217            �           2606    25222 "   prestamo_cab prestamo_cab_dni_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prestamo_cab
    ADD CONSTRAINT prestamo_cab_dni_fkey FOREIGN KEY (dni) REFERENCES public.persona(dni);
 L   ALTER TABLE ONLY public.prestamo_cab DROP CONSTRAINT prestamo_cab_dni_fkey;
       public          postgres    false    217    4738    221            �           2606    25227 (   prestamo_det prestamo_det_cod_libro_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prestamo_det
    ADD CONSTRAINT prestamo_det_cod_libro_fkey FOREIGN KEY (cod_libro) REFERENCES public.libro(cod_libro);
 R   ALTER TABLE ONLY public.prestamo_det DROP CONSTRAINT prestamo_det_cod_libro_fkey;
       public          postgres    false    222    4736    215            �           2606    25232 +   prestamo_det prestamo_det_cod_prestamo_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.prestamo_det
    ADD CONSTRAINT prestamo_det_cod_prestamo_fkey FOREIGN KEY (cod_prestamo) REFERENCES public.prestamo_cab(cod_prestamo);
 U   ALTER TABLE ONLY public.prestamo_det DROP CONSTRAINT prestamo_det_cod_prestamo_fkey;
       public          postgres    false    4744    222    221            '   4  x�e��NA���S4�JLV!oHB����;�`evˎ	�G�|�}1��p�tگZ�Q��^����2E����Y�[Â�x�f�+�g��)��6E�*L�޴��*EN@T�X�蘖a��.�q��\5ߑ�fA�{�	J�(�}t �;{k�#i^�(բ�t�=�Kw�(0!<�~�-̔U_3�mW����AXQ�]��<q)���T-z�ofXS�jv�씗�֭�(J���.U�\�1Qa���S��6�D�*��������fXg];Ʋ��Q\�0k�if��Hyӵo���?j���      .   �   x���11D�:9�:�c߅��Q -T�{x�t_C��nۊ��[W�pL�:I����`�2+�w6�N[�P�J�|�{s�%���5�}j	�]z���5s�֕J#�z[F4���p+�T ��P���05�.��ծ��_9��Nrw      )   �   x�=�1
�@��z�0BA[�"�`e3fXw`��"��<C.梋_��U�\"��Sb#��yg�в3�y'Iz���[qW�5��zON�˙��4��`�Z�;x(��#�&͙u�x�c�x��{f��p"3�9)�7��o�?N      *      x�34� NC.#(�4�2�Nc�=... ~�(      ,   r   x�}���0��..D�q�]���C-�Ƚ���-;�V<
%#@e~w�R'��������oU���n5٧z��S�|�dG�+ٝ<��`�c�����<�,�zPq |��D:      -   b   x�=���0�w2����]x3�;���ǀ5��� RH�;�D�&��1��þ������K�n��㞎Vu��}*���8��Qs�%�܇� %�      +   0   x�3�t�L���/IMN,���2�t�ON�+I�2�t�)�������� ��     