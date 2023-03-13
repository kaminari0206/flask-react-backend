<script>
  // import the fetch function to call the Flask API and get the data
  import { onMount } from 'svelte';
  let events = [];

  onMount(async () => {
    const response = await fetch('/api/events');
    events = await response.json();
  });
</script>

<div class="container">
  {#each events as event, i}
    {#if i % 3 === 0}
      <div class="column">
    {/if}
    <div class="event">
      <h3>{event.name}</h3>
      <p>{event.location}</p>
      <p>{event.time}</p>
      <p>{event.price}</p>
    </div>
    {#if i % 3 === 2 || i === events.length - 1}
      </div>
    {/if}
  {/each}
</div>

<style>
  .container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }

  .column {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    margin: 20px;
  }

  .event {
    width: 300px;
    height: 300px;
    background-color: #f0f0f0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
    margin: 10px;
  }

  h3 {
    margin-top: 0;
  }
</style>






