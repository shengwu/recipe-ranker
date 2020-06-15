import React, { useEffect, useState } from 'react';
import { ICategory } from './types';
import Category from './Category';

const App: React.FC = () => {
  const [categories, setCategories] = useState<Array<ICategory>>([]);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchCategories = async () => {
      // There's some magic happening here: the shape of the JSON response's
      // 'categories' key just happens to fit the shape of Array<ICategory> -
      // each category has a name and an array of recipes. Doesn't feel super
      // safe though:
      // - the server could add a random key to each recipe or each category.
      //   this is actually fine, the types as defined will ignore the extra
      //   attribute.
      // - the frontend could add a required attribute to e.g. ICategory. weird,
      //   i guess there are no errors here either.
      fetch('http://localhost:5000/')
        .then(response => response.json())
        .then(response => setCategories(response.categories))
        .catch(error => setError(error.error));
    };

    fetchCategories();
  }, []);

  return (
    <div>
    { categories === [] ? (
        error === '' ? (<p>Loading...</p>) : (<p>Error: {error}</p>)
      ) : categories.map(
        (category: ICategory) => <Category key={category.name} category={category} />
      )}
    </div>
  );
}

export default App;
