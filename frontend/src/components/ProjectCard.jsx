const ProjectCard = (props) => {
  const { title, status, body } = props;
  return (
    <article className="project-card">
      <h3>{title}</h3>
      <p>{status}</p>
      <p>{body}</p>
    </article>
  );
};

export default ProjectCard;
