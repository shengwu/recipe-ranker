export interface IRecipe {
  url: string;
  votes: number;
}

export interface ICategory {
  name: string;
  recipes: Array<IRecipe>;
}
