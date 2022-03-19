# habi-technical-test
Prueba tecnica Habi
Para el desarrollo de la prueba tecnica haré uso del framework flask, esto debido a:
1. Simplicidad del framework para empezar a trabajar.
2. Experiencia anterior haciendo uso del mismo.
El proceso del desarrollo va principalmente orientado a poder montar de manera satisfactoria el servidor local y 
a configurar de manera correcta la API para atender los requests.
El formatter utilizado fue black formatter.
El manejo de la db se hará mediante sentencias SQL, como se estipuló en el documento de la prueba tecnica.

Durante la realización de la prueba:
Al enfrentarme a los datos con inconsistencias (dirección vacia, ciudad vacia, etc), tomé la decisión de filtrar aquellas
que no tuviesen dirección/ciudad puesto que estos son datos que toda propiedad deberia tener para poder mostrarsela
al cliente. De ser necsario, solo haria falta agregar más filtros a la función filter_incongruent_data para evitar otros casos
(price=0, description=null)

Para correr las pruebas: Estando sobre el repositorio. python -m unittest
Para correr el proyecto: Estando sobre el repositorio. set FLASK_APP=app, flask run

Explicación segundo punto:
Para llevar un control simple de a que propiedades le ha dado "me gusta" un usuario, se hace necesario crear una nueva tabla
en la cual guardar la relación Many2Many entre ambas tablas (un usuario puede darle me gusta a muchas propiedades y
una misma propiedad puede tener muchos me gusta de los usuarios). Ademas, se agrega una propiedad delete (booleano) para
poder "borrar" (soft delete) cuando un usuario decida quitarle el me gusta a alguna de las propiedades. No es necesario 
para el requerimiento, pero tambien podria tenerse la fecha de creación/edición de los registros para así poder mostrar
cronologicamente los me gusta de la propiedad.
Codigo SQL:
CREATE TABLE user_property_rel(
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    delete BIT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (property_id) REFERENCES property(id)
)

Segundo punto opcional:
Como propuesta para mejora, se puede tener un campo "current_status" en la tabla property, campo puede verse relacionado
a un trigger en la tabla status_history y, de esta manera, mantener el estado actual de la propiedad en la tabla property,
facilitando la request de las propiedades disponibles pues ya no seria necesario consultar status_history.
Query actual: 
select * from(
        select 
        p.id, 
        p.address, 
        p.city, 
        p.price, 
        p.description, 
        p.year,
        SUBSTRING_INDEX( GROUP_CONCAT(CAST(sh.status_id AS CHAR) ORDER BY sh.update_date desc), ',', 1 ) AS status_id
        from property p 
        inner join status_history sh 
        on sh.property_id = p.id 
        group by p.id
        ) as information
        where status_id in ('3', '4', '5') 
        + extra filtros
Query resultado del cambio:
select 
id, 
address, 
city, 
price, 
description, 
year,
current_status
from property
where current_status in (3,4,5)
+ extra filtros
        

