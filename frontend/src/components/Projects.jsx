import { useEffect, useState } from "react";
import ProjectCard from "./ProjectCard";

const Projects = () => {
  const [search, setSearch] = useState("");
  const [projects, setProjects] = useState([]);

  const handleInput = (e) => {
    setSearch(e.target.value);
  };

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/v1/project/get/all",
        );
        const data = await response.json();

        setProjects(data);
      } catch (error) {
        console.log("3");
      } finally {
        console.log("3");
      }
    };
    fetchProjects();
  }, []);

  return (
    <div className="container">
      <h2>Добро пожавловать в Boardly!</h2>

      <input
        type="text"
        placeholder="Search project..."
        className="search-input"
        value={search}
        onChange={handleInput}
      />

      <section className="projects">
        {projects && projects.length > 0 ? (
          projects.map((project) => (
            <ProjectCard
              key={project.id}
              title={project.name}
              status={project.status}
              body={project.description}
            />
          ))
        ) : (
          <p style={{ marginTop: "1rem", color: "#888" }}>No projectss</p>
        )}
      </section>
    </div>
  );
};

export default Projects;
