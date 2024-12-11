
CREATE TABLE public.genome_scores (
    genome_score_id integer NOT NULL,
    movie_id integer NOT NULL,
    genome_tag_id integer NOT NULL,
    relevance integer NOT NULL
);


ALTER TABLE public.genome_scores OWNER TO "user";


CREATE SEQUENCE public.genome_scores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genome_scores_id_seq OWNER TO "user";
ALTER SEQUENCE public.genome_scores_id_seq OWNED BY public.genome_scores.genome_score_id;


CREATE TABLE public.genome_tags (
    genome_tag_id integer NOT NULL,
    tag character varying NOT NULL
);


ALTER TABLE public.genome_tags OWNER TO "user";

CREATE SEQUENCE public.genome_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genome_tags_id_seq OWNER TO "user";
ALTER SEQUENCE public.genome_tags_id_seq OWNED BY public.genome_tags.genome_tag_id;

CREATE TABLE public.genres (
    genre_id integer NOT NULL,
    name character varying(100) NOT NULL
);

ALTER TABLE public.genres OWNER TO "user";

CREATE SEQUENCE public.genres_genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genres_genre_id_seq OWNER TO "user";
ALTER SEQUENCE public.genres_genre_id_seq OWNED BY public.genres.genre_id;


CREATE TABLE public.movie_genre (
    movie_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.movie_genre OWNER TO "user";

CREATE TABLE public.movie_info (
    imdb_id integer NOT NULL,
    year integer,
    director character varying(255),
    description text,
    title character varying(255)
);


ALTER TABLE public.movie_info OWNER TO "user";

CREATE TABLE public.movies (
    movie_id integer NOT NULL,
    title character varying NOT NULL,
    imdb_id integer
);


ALTER TABLE public.movies OWNER TO "user";

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movies_id_seq OWNER TO "user";
ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.movie_id;

CREATE TABLE public.ratings (
    rating_id integer NOT NULL,
    user_id integer,
    movie_id integer,
    rating real NOT NULL,
    rated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.ratings OWNER TO "user";

CREATE SEQUENCE public.ratings_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ratings_rating_id_seq OWNER TO "user";
ALTER SEQUENCE public.ratings_rating_id_seq OWNED BY public.ratings.rating_id;

CREATE TABLE public.tags (
    tag_id integer NOT NULL,
    user_id integer NOT NULL,
    movie_id integer NOT NULL,
    tag character varying NOT NULL,
    "time" timestamp without time zone
);


ALTER TABLE public.tags OWNER TO "user";

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO "user";
ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.tag_id;

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50),
    email character varying(100),
    password character varying(256),
    role character varying(10),
    registered_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO "user";

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO "user";
ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
ALTER TABLE ONLY public.genome_scores ALTER COLUMN genome_score_id SET DEFAULT nextval('public.genome_scores_id_seq'::regclass);
ALTER TABLE ONLY public.genome_tags ALTER COLUMN genome_tag_id SET DEFAULT nextval('public.genome_tags_id_seq'::regclass);
ALTER TABLE ONLY public.genres ALTER COLUMN genre_id SET DEFAULT nextval('public.genres_genre_id_seq'::regclass);
ALTER TABLE ONLY public.movies ALTER COLUMN movie_id SET DEFAULT nextval('public.movies_id_seq'::regclass);
ALTER TABLE ONLY public.ratings ALTER COLUMN rating_id SET DEFAULT nextval('public.ratings_rating_id_seq'::regclass);
ALTER TABLE ONLY public.tags ALTER COLUMN tag_id SET DEFAULT nextval('public.tags_id_seq'::regclass);
ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
ALTER TABLE ONLY public.genome_scores
    ADD CONSTRAINT genome_scores_pkey PRIMARY KEY (genome_score_id);

ALTER TABLE ONLY public.genome_tags
    ADD CONSTRAINT genome_tags_pkey PRIMARY KEY (genome_tag_id);

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_name_key UNIQUE (name);

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (genre_id);

ALTER TABLE ONLY public.movie_genre
    ADD CONSTRAINT movie_genre_pkey PRIMARY KEY (movie_id, genre_id);

ALTER TABLE ONLY public.movie_info
    ADD CONSTRAINT movie_info_pkey PRIMARY KEY (imdb_id);

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (movie_id);

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (rating_id);

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY public.genome_scores
    ADD CONSTRAINT fk_genome_tag_id FOREIGN KEY (genome_tag_id) REFERENCES public.genome_tags(genome_tag_id);

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT fk_imdb_id FOREIGN KEY (imdb_id) REFERENCES public.movie_info(imdb_id);

ALTER TABLE ONLY public.genome_scores
    ADD CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES public.movies(movie_id);

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT fk_user_rating FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT fk_user_tag FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.movie_genre
    ADD CONSTRAINT movie_genre_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(genre_id) ON DELETE CASCADE;


ALTER TABLE ONLY public.movie_genre
    ADD CONSTRAINT movie_genre_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(movie_id) ON DELETE CASCADE;

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(movie_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.tags
    ADD CONSTRAINT "tags_movieID_fkey" FOREIGN KEY (movie_id) REFERENCES public.movies(movie_id);

-- public.movies_with_info исходный текст

CREATE OR REPLACE VIEW public.movies_with_info
AS SELECT m.movie_id,
    m.title AS movie_title,
    mi.year,
    mi.director,
    mi.description,
    mi.title AS info_title,
    array_agg(DISTINCT g.name) AS genres,
    avg(r.rating) AS average_rating
   FROM movies m
     LEFT JOIN movie_info mi ON m.imdb_id = mi.imdb_id
     LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
     LEFT JOIN genres g ON mg.genre_id = g.genre_id
     LEFT JOIN ratings r ON m.movie_id = r.movie_id
  GROUP BY m.movie_id, mi.year, mi.director, mi.description, mi.title;

-- Permissions

ALTER TABLE public.movies_with_info OWNER TO "user";
GRANT ALL ON TABLE public.movies_with_info TO "user";