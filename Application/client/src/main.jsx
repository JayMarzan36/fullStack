import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import 'vite/modulepreload-polyfill';

import { createHashRouter, RouterProvider } from 'react-router';

import { NewNote } from './pages/NewNote.jsx';
import { ViewNotes } from './pages/ViewNotes.jsx';
import { Graph } from './components/Graph.jsx';


const router = createHashRouter([
  {
    path: "/",
    element: <App/>,
    children: [
      {
        path: "/",
        element: <Graph/>
      },
      {
        path: "/newnote",
        element: <NewNote/>,
      },
      {
        path: "/viewnote",
        element: <ViewNotes/>,
      }
    ]
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(

    <RouterProvider router={router}/>
  
)