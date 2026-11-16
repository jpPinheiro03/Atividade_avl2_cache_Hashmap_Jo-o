package school.sptech.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import school.sptech.entity.Conteudo;

public interface ConteudoRepository extends JpaRepository<Conteudo, Long> {
}
