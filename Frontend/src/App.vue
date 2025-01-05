// src/components/Dashboard.vue
<template>
  <div class="min-h-screen bg-gray-100">
    <div class="container mx-auto px-4 py-8">
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div v-for="(metric, index) in summaryMetrics" :key="index"
          class="card bg-white shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-lg">{{ metric.label }}</h2>
            <p class="text-2xl font-bold">{{ metric.value }}</p>
          </div>
        </div>
      </div>

      <!-- Project Input Form -->
      <div class="card bg-white shadow-xl mb-8">
        <div class="card-body">
          <h2 class="card-title mb-4">Add New Project</h2>
          <form @submit.prevent="submitProject" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="form-control">
              <label class="label">Project Name</label>
              <input v-model="newProject.name" type="text" class="input input-bordered" required />
            </div>
            <div class="form-control">
              <label class="label">Budget</label>
              <input v-model="newProject.budget" type="number" class="input input-bordered" required />
            </div>
            <div class="form-control">
              <label class="label">CO2 Reduction (tons)</label>
              <input v-model="newProject.expected_co2_reduction" type="number" class="input input-bordered" required />
            </div>
            <div class="form-control">
              <label class="label">Social Impact Score (0-100)</label>
              <input v-model="newProject.social_impact_score" type="number" min="0" max="100" class="input input-bordered" required />
            </div>
            <div class="form-control md:col-span-2">
              <label class="label">Description</label>
              <textarea v-model="newProject.description" class="textarea textarea-bordered" required></textarea>
            </div>
            <div class="form-control md:col-span-2">
              <button type="submit" class="btn btn-primary">Add Project</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Projects Table -->
      <div class="card bg-white shadow-xl">
        <div class="card-body">
          <h2 class="card-title mb-4">Project Portfolio</h2>
          <div class="overflow-x-auto">
            <table class="table w-full">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Budget</th>
                  <th>ESG Score</th>
                  <th>CO2 Reduction</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="project in projects" :key="project.id">
                  <td>{{ project.name }}</td>
                  <td>${{ formatNumber(project.budget) }}</td>
                  <td>
                    <div class="radial-progress" :style="{ '--value': project.esg_score }">
                      {{ Math.round(project.esg_score) }}
                    </div>
                  </td>
                  <td>{{ formatNumber(project.expected_co2_reduction) }} tons</td>
                  <td>
                    <button @click="analyzeProject(project.id)" class="btn btn-sm btn-info mr-2">
                      Analyze
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
  name: 'Dashboard',
  setup() {
    const projects = ref([]);
    const summaryMetrics = ref([]);
    const newProject = ref({
      name: '',
      description: '',
      budget: 0,
      expected_co2_reduction: 0,
      social_impact_score: 0,
      governance_score: 50, // Default value
      timeline_months: 12, // Default value
    });

    const API_URL = 'http://localhost:8000';

    const fetchProjects = async () => {
      try {
        const response = await axios.get(`${API_URL}/projects/`);
        projects.value = response.data;
      } catch (error) {
        console.error('Error fetching projects:', error);
      }
    };

    const fetchSummary = async () => {
      try {
        const response = await axios.get(`${API_URL}/dashboard/summary`);
        const data = response.data;
        summaryMetrics.value = [
          { label: 'Total Projects', value: data.total_projects },
          { label: 'Total Budget', value: `$${formatNumber(data.total_budget)}` },
          { label: 'Average ESG Score', value: `${Math.round(data.average_esg_score)}%` },
          { label: 'Total CO2 Reduction', value: `${formatNumber(data.total_co2_reduction)} tons` },
        ];
      } catch (error) {
        console.error('Error fetching summary:', error);
      }
    };

    const submitProject = async () => {
      try {
        await axios.post(`${API_URL}/projects/`, newProject.value);
        await fetchProjects();
        await fetchSummary();
        newProject.value = {
          name: '',
          description: '',
          budget: 0,
          expected_co2_reduction: 0,
          social_impact_score: 0,
          governance_score: 50,
          timeline_months: 12,
        };
      } catch (error) {
        console.error('Error submitting project:', error);
      }
    };

    const analyzeProject = async (projectId) => {
      try {
        const response = await axios.post(`${API_URL}/analyze/project/${projectId}`);
        // Handle the analysis results - you could show them in a modal or update the UI
        console.log(response.data);
      } catch (error) {
        console.error('Error analyzing project:', error);
      }
    };

    const formatNumber = (num) => {
      return new Intl.NumberFormat().format(num);
    };

    onMounted(() => {
      fetchProjects();
      fetchSummary();
    });

    return {
      projects,
      summaryMetrics,
      newProject,
      submitProject,
      analyzeProject,
      formatNumber,
    };
  },
};
</script>